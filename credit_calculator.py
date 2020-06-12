import argparse
from math import ceil, log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str)
    parser.add_argument("--payment", type=int)
    parser.add_argument("--principal", type=int)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)

    args = vars(parser.parse_args())
    valid_args = check_args(args)
    if valid_args:
        if args["type"] == "annuity":
            annuity_payment(args)
        else:
            diff_payment(args)
    else:
        print("Incorrect parameters")


def check_args(args_list):
    invalid = (len([value for value in args_list.values() if value is not None]) < 4 or args_list["interest"] is None
               or args_list["type"] not in ("annuity", "diff") or args_list["type"] == "diff" and args_list["payment"]
               or args_list["interest"] < 0)

    return not invalid


def ann_principal(args_list):
    i = args_list["interest"] / (100 * 12)
    n = args_list["periods"]
    a = args_list["payment"]
    p = a * ((1 + i) ** n - 1) / (i * (1 + i) ** n)
    print(f"Your credit principal = {int(p)}!")
    print(f"Overpayment = {ceil(n * a - p)}")


def ann_periods(args_list):
    i = args_list["interest"] / (100 * 12)
    a = args_list["payment"]
    p = args_list["principal"]
    n = ceil(log(a / (a - i * p), 1 + i))
    years, months = divmod(n, 12)
    if years and months:
        print(f"You need {years} years and {months} months to repay this credit!")
    elif years:
        print(f"You need {years} years to repay this credit!")
    else:
        print(f"You need {months} months to repay this credit!")
    print(f"Overpayment = {n * a - p}")


def ann_month_pay(args_list):
    i = args_list["interest"] / (100 * 12)
    p = args_list["principal"]
    n = args_list["periods"]
    a = p * i * (1 + i) ** n / ((1 + i) ** n - 1)
    print(f"Your annuity payment = {ceil(a)}!")
    print(f"Overpayment = {n * ceil(a) - p}")


def annuity_payment(args_list):
    to_calculate = [key for key in args_list.keys() if args_list[key] is None][0]
    if to_calculate == "principal":
        ann_principal(args_list)
    elif to_calculate == "periods":
        ann_periods(args_list)
    else:
        ann_month_pay(args_list)


def diff_payment(args_list):
    total_pay = 0
    if args_list["principal"] < 0 or args_list["periods"] < 0:
        print("Incorrect parameters")
        return
    i = args_list["interest"] / (100 * 12)
    p = args_list["principal"]
    n = args_list["periods"]
    for m in range(1, n + 1):
        d_m = ceil(p / n + i * (p - p * (m - 1) / n))
        print(f"Month {m}: paid out {d_m}")
        total_pay += d_m
    print(f"Overpayment = {total_pay - p}")


if __name__ == '__main__':
    main()

