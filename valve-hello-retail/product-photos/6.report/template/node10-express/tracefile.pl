#!/usr/bin/perl

=head1 NAME

tracefile - list files being accessed

=head1 SYNOPSIS

B<tracefile> [-adeflnruw] I<command>

B<tracefile> [-adeflnruw] -p I<pid>

=head1 DESCRIPTION

B<tracefile> will print the files being accessed by the command.

=head1 OPTIONS

=over 12

=item I<command>

Command to run.


=item B<-a>

=item B<--all>

List all files.


=item B<-d>

=item B<--dir>

List only dirs.


=item B<-e>

=item B<--exist>

List only existing files.


=item B<-f>

=item B<--file>

List only normal files.


=item B<-l>

=item B<--local>

List only files in current directory. Useful to avoid matching at
system files.


=item B<-n>

=item B<--nonexist>

List only non-existing files.


=item B<-p> I<pid>

=item B<--pid> I<pid>

Trace process id.


=item B<-u>

=item B<--unique>

List only files once.


=item B<-r>

=item B<--read>

List only files being access for reading.


=item B<-w>

=item B<--write>

List only files being access for writing.


=back


=head1 EXAMPLES

=head2 EXAMPLE: Find the missing package

Assume you have a program B<foo>. When it runs it fails with: I<foo:
error: missing library>. It does not say with file is missing, but you
have a hunch that you just need to install a package - you just do not
know which one.

    tracefile -n -u foo | apt-file -f search -

Here B<ls> tries to find B</usr/include/shisa.h>. If it fails,
B<apt-file> will search for which package it is in:

    tracefile -n -u ls /usr/include/shisa.h | apt-file -f search - |
      grep /usr/include/shisa.h

=head1 REPORTING BUGS

Report bugs to <tange@gnu.org>.


=head1 AUTHOR

Copyright (C) 2012-2019 Ole Tange, http://ole.tange.dk and Free
Software Foundation, Inc.


=head1 LICENSE

Copyright (C) 2012 Free Software Foundation, Inc.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
at your option any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=head2 Documentation license I

Permission is granted to copy, distribute and/or modify this documentation
under the terms of the GNU Free Documentation License, Version 1.3 or
any later version published by the Free Software Foundation; with no
Invariant Sections, with no Front-Cover Texts, and with no Back-Cover
Texts.  A copy of the license is included in the file fdl.txt.

=head2 Documentation license II

You are free:

=over 9

=item B<to Share>

to copy, distribute and transmit the work

=item B<to Remix>

to adapt the work

=back

Under the following conditions:

=over 9

=item B<Attribution>

You must attribute the work in the manner specified by the author or
licensor (but not in any way that suggests that they endorse you or
your use of the work).

=item B<Share Alike>

If you alter, transform, or build upon this work, you may distribute
the resulting work only under the same, similar or a compatible
license.

=back

With the understanding that:

=over 9

=item B<Waiver>

Any of the above conditions can be waived if you get permission from
the copyright holder.

=item B<Public Domain>

Where the work or any of its elements is in the public domain under
applicable law, that status is in no way affected by the license.

=item B<Other Rights>

In no way are any of the following rights affected by the license:

=over 2

=item *

Your fair dealing or fair use rights, or other applicable
copyright exceptions and limitations;

=item *

The author's moral rights;

=item *

Rights other persons may have either in the work itself or in
how the work is used, such as publicity or privacy rights.

=back

=back

=over 9

=item B<Notice>

For any reuse or distribution, you must make clear to others the
license terms of this work.

=back

A copy of the full license is included in the file as cc-by-sa.txt.

=head1 DEPENDENCIES

B<tracefile> uses Perl, and B<strace>.


=head1 SEE ALSO

B<strace>(1)

=cut

use Getopt::Long;

$Global::progname = "tracefile";

Getopt::Long::Configure("bundling","require_order");
get_options_from_array(\@ARGV) || die_usage();
init_functions();

my @cmd = shell_quote(@ARGV);
my $dir = ".";
my $pid = $opt::pid ? "-p $opt::pid" : "";

# BUG: If command gives output on stderr that can confuse the strace output
open(IN, "-|", "strace -ff $pid -e trace=file @cmd 2>&1 >/dev/null") || die;
while(<IN>) {
    if(/chdir."(([^\\"]|\\[\\"nt])*)".\s*=\s*0/) {
	$dir = $1;
    }
    # [pid 30817] stat("t/tar.gz", {st_mode=S_IFREG|0644, st_size=140853248, ...}) = 0
    # openat(AT_FDCWD, "/tmp/a", O_WRONLY|O_CREAT|O_NOCTTY|O_NONBLOCK, 0666) = 3
    if(/^(\[[^]]+\])? # Match pid
       \s*([^\" ]+)   # function
       [(]            # (
       [^"]*          # E.g. AT_FDCWD
       "              # "
       (([^\\"]|\\[\\"nt])*) # content of string with \n \" \t \\
       "(.*)/x)     # Rest
    {
	# Matches the strace structure for a file
	my $function = $2;
	my $file = shell_unquote($3);
	my $addinfo = $5;
	# Relative to $dir
	$file =~ s:^([^/]):$dir/$1:;
	$file =~ s:/./:/:g; # /./ => /
	$file =~ s:/[^/]+/\.\./:/:g; # /foo/../ => /
	# Match files in $PWD or starting with ./
	my $local = ($file =~ m<^(\Q$ENV{'PWD'}\E|\./)>);
	my $read = readfunc($function,$addinfo);
	my $write = writefunc($function,$addinfo);
	my $print = 1;
	if(($opt::read and not $read)
	   or
	   ($opt::write and not $write)
	   or
	   ($opt::dir and not -d $file)
	   or
	   ($opt::file and not -f $file)
	   or
	   ($opt::exists and not -e $file)
	   or
	   ($opt::local and not $local)
	   or
	   ($opt::nonexists and -e $file)
	   or
	   ($opt::unique and $seen{$file}++)) {
	    $print = 0;
	}
	$print and print $file,"\n";
    }    
}

{
    my %warned;
    my %funcs;
    
    sub init_functions {
	# function name => r/w/rw/n/?
	# r = read
	# w = write
	# rw = read+write
	# n = neither (false match)
	# ? = TODO figure out what they do
	%funcs =
	    qw(access r acct ? chdir r chmod w chown w chown16 w
	       chroot r creat w execv r execve r execveat r faccessat
	       r fanotify_mark ? fchmodat w fchownat w fstat r fstat64
	       r fstatat64 r fstatfs r fstatfs64 r futimesat r getcwd
	       r getxattr r inotify_add_watch r link w linkat w
	       listxattr r lstat r lstat64 r mkdir w mkdirat w mknod w
	       mknodat w mount r name_to_handle_at ?  newfstatat r
	       oldfstat r oldlstat r oldstat r open rw openat rw
	       osf_fstatfs r osf_statfs r osf_utimes r perror n pivotroot r
	       printargs ? printf n quotactl ?  readlink r readlinkat r
	       removexattr w rename w renameat w renameat2 w rmdir w
	       setxattr w stat r stat64 r statfs r statfs64 r statx r
	       swapoff w swapon w symlink w symlinkat w truncate w
	       truncate64 w umount r umount2 r unlink w unlinkat w
	       uselib r utime w utimensat w utimes w);
    }

    sub readfunc {
	# The call is a call that would work on a RO file system
	my($func,$info) = @_;
	if($func eq "open" or $func eq "openat") {
	    return ($info=~/O_RDONLY/);
	}
	if($funcs{$func}) {
	    return ($funcs{$func} eq "r");
	} else {
	    $warned{$func}++ or
		warning("'$func' is unknown. Please report at",
			"https://gitlab.com/ole.tange/tangetools/issues");
	    return 0;
	}
    }

    sub writefunc {
	# The call is a call that would need RW file system
	my($func,$info) = @_;
	if($func eq "open" or $func eq "openat") {
	    return ($info=~/O_WRONLY|O_APPEND|O_CREAT/);
	}
	if($funcs{$func}) {
	    return ($funcs{$func} eq "w");
	} else {
	    $warned{$func}++ or
	    warning("$func is unknown. Please report at",
		    "https://gitlab.com/ole.tange/tangetools/issues");
	    return 0;
	}
    }
}

sub options_hash {
    # Returns a hash of the GetOptions config
    return
	("debug|D" => \$opt::debug,
	 "dir|d" => \$opt::dir,
	 "file|f" => \$opt::file,
	 "uniq|unique|u" => \$opt::unique,
         "exists|exist|e" => \$opt::exists,
         "nonexists|nonexist|non-exists|non-exist|n" => \$opt::nonexists,
	 "local|l" => \$opt::local,
	 "read|r" => \$opt::read,
	 "write|w" => \$opt::write,
         "all|a" => \$opt::all,
	 "pid|p=i" => \$opt::pid,
	);
}

sub get_options_from_array {
    # Run GetOptions on @array
    # Returns:
    #   true if parsing worked
    #   false if parsing failed
    #   @array is changed
    my $array_ref = shift;
    # A bit of shuffling of @ARGV needed as GetOptionsFromArray is not
    # supported everywhere
    my @save_argv;
    my $this_is_ARGV = (\@::ARGV == $array_ref);
    if(not $this_is_ARGV) {
	@save_argv = @::ARGV;
	@::ARGV = @{$array_ref};
    }
    my @retval = GetOptions(options_hash());
    if(not $this_is_ARGV) {
	@{$array_ref} = @::ARGV;
	@::ARGV = @save_argv;
    }
    return @retval;
}

sub shell_unquote {
    # Unquote strings from shell_quote
    # Returns:
    #   string with shell quoting removed
    my @strings = (@_);
    my $arg;
    for my $arg (@strings) {
        if(not defined $arg) {
            $arg = "";
        }
        $arg =~ s/'\n'/\n/g; # filenames with '\n' is quoted using \'
        $arg =~ s/\\([\002-\011\013-\032])/$1/g;
        $arg =~ s/\\([\#\?\`\(\)\{\}\*\>\<\~\|\; \"\!\$\&\'])/$1/g;
        $arg =~ s/\\\\/\\/g;
    }
    return wantarray ? @strings : "@strings";
}

sub shell_quote {
    my @strings = (@_);
    for my $a (@strings) {
        $a =~ s/([\002-\011\013-\032\\\#\?\`\(\)\{\}\[\]\*\>\<\~\|\; \"\!\$\&\'\202-\377])/\\$1/g;
        $a =~ s/[\n]/'\n'/g; # filenames with '\n' is quoted using \'
    }
    return wantarray ? @strings : "@strings";
}

sub die_usage {
    # Returns: N/A
    usage();
    wait_and_exit(255);
}

sub usage {
    # Returns: N/A
    print join
	("\n",
	 "Usage:",
	 "$Global::progname [-u] [-a] [-n] [-e] command [arguments]",
	 "",
	 "See 'man $Global::progname' for details",
	 "");
}

sub warning {
    my @w = @_;
    my $fh = $Global::original_stderr || *STDERR;
    my $prog = $Global::progname || "tracefile";
    print $fh map { ($prog, ": Warning: ", $_, "\n"); } @w;
}


sub error {
    my @w = @_;
    my $fh = $Global::original_stderr || *STDERR;
    my $prog = $Global::progname || "tracefile";
    print $fh $prog, ": Error: ", @w;
}

sub my_dump(@) {
    # Returns:
    #   ascii expression of object if Data::Dump(er) is installed
    #   error code otherwise
    my @dump_this = (@_);
    eval "use Data::Dump qw(dump);";
    if ($@) {
        # Data::Dump not installed
        eval "use Data::Dumper;";
        if ($@) {
            my $err =  "Neither Data::Dump nor Data::Dumper is installed\n".
                "Not dumping output\n";
            ::status($err);
            return $err;
        } else {
            return Dumper(@dump_this);
        }
    } else {
	# Create a dummy Data::Dump:dump as Hans Schou sometimes has
	# it undefined
	eval "sub Data::Dump:dump {}";
        eval "use Data::Dump qw(dump);";
        return (Data::Dump::dump(@dump_this));
    }
}

