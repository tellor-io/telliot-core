'''Submits three month rolling average of the USPCE to TellorX on Rinkeby.'''


def submit():
    print('Enter USPCE value (example: 13659.3:')

    uspce = None

    while uspce is None:
        inpt = input()

        try:
            inpt = int(float(inpt) * 1000000)
        except ValueError:
            print('Invalid input. Enter int or float.')
            continue

        _ = input(f'Submitting value: {inpt}\nPress [ENTER] to confirm.')

        uspce = inpt

    # submit input value
    
    # print success/fail & rinkebyscan link
    print(f'Success. See here: {uspce}')


if __name__ == "__main__":
    submit()