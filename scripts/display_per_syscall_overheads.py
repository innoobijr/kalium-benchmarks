#!/usr/bin/python3

import sys
import statistics

def usage():
    print ("python3 display_per_syscall_overheads.py <runsc_boot_log_file>")
    exit(1)


def conv_to_secs(val):
    val = val.strip()
    v = 0.0
    multiplier = 1
    if val[-2:] == "µs":
        multiplier = 10 ** -6
        v = float(val[:-2]) * multiplier
    elif val[-2:] == "ms":
        multiplier = 10 ** -3
        v = float(val[:-2]) * multiplier
    else:
        v = float(val[:-2])
    return v


def main():
    if len(sys.argv) != 2:
        usage()

    runsc_log_filename = sys.argv[1]
    f = open(runsc_log_filename, "r")

    # Values in seconds
    write_syscall_stats = {
            'tls_parsing' : [],
            'tls_lookup' : [],
            'event_construction': [],
            'local_guard': [],
            'global_ctr': [],
            'tot_syscall': []
    }

    sendmsg_syscall_stats = {
            'tls_parsing' : [],
            'tls_lookup' : [],
            'event_construction': [],
            'local_guard': [],
            'global_ctr': [],
            'tot_syscall': []
    }

    aes_gcm_encrypt_tot = []
    count_enc = 0

    count_write = 0
    count_sendmsg = 0

    for line in f.readlines():
        line = line.strip()
        if "GETEValidateWriteMeasure" in line:
            count_write += 1
            vals = list(map(conv_to_secs, line.split("[GETEValidateWriteMeasure]")[1].strip().split(':')))
            print (vals)
            write_syscall_stats['tls_parsing'] += [vals[0]]
            write_syscall_stats['tls_lookup'] += [vals[1]]
            write_syscall_stats['event_construction'] += [vals[2]]
            write_syscall_stats['local_guard'] += [vals[4]]
            write_syscall_stats['global_ctr'] += [vals[3]]
            write_syscall_stats['tot_syscall'] += [vals[6]]

        if "GETEValidateSendMsgMeasure" in line:
            count_sendmsg += 1
            vals = list(map(conv_to_secs, line.split("[GETEValidateSendMsgMeasure]")[1].strip().split(':')))
            print (vals)
            sendmsg_syscall_stats['tls_parsing'] += [vals[0]]
            sendmsg_syscall_stats['tls_lookup'] += [vals[1]]
            sendmsg_syscall_stats['event_construction'] += [vals[2]]
            sendmsg_syscall_stats['local_guard'] += [vals[4]]
            sendmsg_syscall_stats['global_ctr'] += [vals[3]]
            sendmsg_syscall_stats['tot_syscall'] += [vals[6]]

        if "AES_GCM_encrypt_measure" in line:
            count_enc += 1
            v = conv_to_secs(line.split("[AES_GCM_encrypt_measure]")[1].strip())
            aes_gcm_encrypt_tot += [v]



    #print (sendmsg_syscall_stats)
    #print (write_syscall_stats)
    #print (aes_gcm_encrypt_tot)
            

    if count_sendmsg > 0:
        print ("SendMsg Stats:")
        for key in sendmsg_syscall_stats:
            mean = statistics.fmean(sendmsg_syscall_stats[key])
            stdev = 0.0
            if count_sendmsg > 1:
                stdev = statistics.stdev(sendmsg_syscall_stats[key])
            low = sendmsg_syscall_stats[key][0]
            high = sendmsg_syscall_stats[key][0]
            for elem in sendmsg_syscall_stats[key]:
                if elem < low:
                    low = elem
                if elem > high:
                    high = elem

            print ("%s Min: %f, Max: %f, Mean: %f, Stdev: %f" % (key, low, high, mean, stdev))
    print ('------')
    if count_write > 0:
        print ("Write Stats:")
        for key in write_syscall_stats:
            mean = statistics.fmean(write_syscall_stats[key])
            stdev = 0.0
            if count_write > 1:
                stdev = statistics.stdev(write_syscall_stats[key])
            low = write_syscall_stats[key][0]
            high = write_syscall_stats[key][0]
            for elem in write_syscall_stats[key]:
                if elem < low:
                    low = elem
                if elem > high:
                    high = elem

            print ("%s Min: %f, Max: %f, Mean: %f, Stdev: %f" % (key, low, high, mean, stdev))
    print ('------')
    if count_enc > 0:
        print ("AES_GCM_ENC Stats")
        low = aes_gcm_encrypt_tot[0]
        high = aes_gcm_encrypt_tot[0]
        mean = statistics.fmean(aes_gcm_encrypt_tot)
        stdev = 0.0
        if count_enc > 1:
            stdev = statistics.stdev(aes_gcm_encrypt_tot)
        for elem in aes_gcm_encrypt_tot:
                if elem < low:
                    low = elem
                if elem > high:
                    high = elem

        print ("%s Min: %f, Max: %f, Mean: %f, Stdev: %f" % (key, low, high, mean, stdev))

main()
