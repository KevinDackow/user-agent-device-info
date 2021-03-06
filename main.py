"""Contains the REPL and command line interactions"""
import argparse
import get_dev_info as gdi

def handle_args(ua, args):
    """Returns an output string"""
    dev1, dev2 = gdi.ua_to_device_name(ua)
    dev = dev1
    print("Dev1 is:")
    print(dev1)
    try:
        title, data = gdi.get_dev_data(dev1, 'tmp')
    except:
        try:
            title, data = gdi.get_dev_data(dev2, 'tmp')
            dev = dev2
        except:
            print("Unable to identify device.")
            return 
    output = 'Device Identified: ' + title + '\n'
    if args.mem:
        output += "RAM:\n  " + str(gdi.get_ram(gdi.get_memory(data))) + ' MB\n'
    if args.cpu:
        cpu = gdi.get_cpu(data)
        clock = gdi.get_clock_speed(cpu)
        output += "CPU:\n" + "  Clock speed: "
        if clock is not None:
            output += str(clock) + ' GHz\n'
        else:
            output += "Not available.\n"
        cores = gdi.get_cores(cpu)
        output += '  Number of Cores: '
        if cores is not None:
            output += str(cores) + '\n'
        else:
            output += "Not available.\n"
    if args.year:
        output += 'YearClass:\n'
        output += '  ' + str(gdi.get_year_class(data)) + '\n'
    gdi.get_year_class(dev)
    return output

def repl(args):
    """Searches and returns device year class in
    a REPL format"""
    while True:
        try:
            ua = input(">> Input User Agent: ")
            out = handle_args(ua, args)
            if args.output_file is not None:
                with open(args.o, 'a+') as output_file:
                    output_file.write(out)
                print("Successfully written to output file.")
            else:
                print(out)
        except EOFError:
            print("Exiting.")
            break

def no_repl(args):
    """Handles file input with no repl"""
    if args.ua is not None and args.output_file is not None:
        with open(args.ua, 'r') as ua_file:
            with open(args.output_file, 'w+') as output:
                for ua in ua_file:
                    output.write(ua + '\n' + handle_args(ua, args))
    elif args.ua is not None:
        with open(args.ua, 'r') as ua_file:
            for ua in ua_file:
                print(handle_args(ua, args))
    else:
        print("No input file provided. Exiting")

def parse_args():
    """Setups argument parsing for command line interactions"""
    parser = argparse.ArgumentParser(description='Get information from UA String', add_help=True)
    parser.add_argument('-s',
                        action='store_true',
                        dest='sh',
                        help='Begins a UA parsing REPL')
    parser.add_argument('-m', '--memory',
                        action='store_true',
                        dest='mem',
                        help='Get memory information for device')
    parser.add_argument('-c', '--cpu',
                        action='store_true',
                        dest='cpu',
                        help='Get cpu information for a UA string')
    parser.add_argument('-y', '--yearclass',
                        action='store_true',
                        dest='year',
                        help='Get yearclass for a UA string')
    parser.add_argument('-u', '--useragentfile',
                        action='store',
                        dest='ua',
                        help='Provide a file path with \
                             user agents to be automatically processed.')
    parser.add_argument('-o', '--outputfile',
                        action='store',
                        dest='output_file',
                        help='Output file path for processed data.')
    args = parser.parse_args()
    if args.sh and args.ua is not None:
        parser.error('Cannot currently run shell with file input.')
    if args.sh:
        repl(args)
    else:
        no_repl(args)

if __name__ == "__main__":
    parse_args()
