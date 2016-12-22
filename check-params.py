import sys
import yaml
import argparse
import logging

LOG = logging.getLogger('check-params')

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--continue', '-c', action='store_true', dest='_continue')
    p.add_argument('--debug', '-d',
                   dest='loglevel',
                   action='store_const',
                   const='DEBUG')
    p.add_argument('--verbose', '-v',
                   dest='loglevel',
                   action='store_const',
                   const='INFO')
    p.add_argument('input', nargs='+')
    p.set_defaults(loglevel='WARNING')
    return p.parse_args()


def verify_params(here, params=None):
    if isinstance(here, dict):
        for k, v in here.items():
            if k == 'get_param':
                if isinstance(v, str) and v not in params:
                    raise KeyError(v)
            elif isinstance(v, (list, dict)):
                verify_params(v, params=params)
    elif isinstance(here, list):
        for item in here:
            verify_params(item, params=params)


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    for path in args.input:
        LOG.info('checking %s', path)
        try:
            with open(path) as fd:
                template = yaml.load(fd)
            verify_params(template, params=template['parameters'])
        except KeyError as e:
            LOG.error('Unknown parameter in %s: %s',
                      path, e)
            if not args._continue:
                sys.exit(1)
        except yaml.parser.ParserError as e:
            LOG.error('Failed to parse %s: %s', path, e)
            if not args._continue:
                sys.exit(1)

if __name__ == '__main__':
    main()
