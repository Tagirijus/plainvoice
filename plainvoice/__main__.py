'''
Creating invoices and quotes with a plaintext mindset.

Author: Manuel Senfft (www.tagirijus.de)
'''


def main():
    from plainvoice.controller.commands import cli
    cli.pv_cli(prog_name='plainvoice')


if __name__ == '__main__':
    main()
