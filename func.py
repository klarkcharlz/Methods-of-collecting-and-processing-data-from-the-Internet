
def pars_salary(salary: str) -> tuple:
    try:
        if salary:
            temp1 = salary.split(" – ")
            if len(temp1) == 2:
                min_salary = " ".join(temp1[0].split("\u202f"))
                temp2 = temp1[1].split("\u202f")
                max_salary = f"{temp2[0]} {temp2[1].split(' ')[0]}"
                currency = temp2[1].split(' ')[1]
                return min_salary, max_salary, currency
            if len(temp1) == 1:
                temp2 = temp1[0].split(" ")
                if temp2[0] == "до":
                    min_salary = None
                    max_salary = " ".join(temp2[1].split("\u202f"))
                    currency = temp2[2]
                elif temp2[0] == "от":
                    min_salary = " ".join(temp2[1].split("\u202f"))
                    max_salary = None
                    currency = temp2[2]
                return min_salary, max_salary, currency
    except Exception as err:
        print(f"{type(err)}:\n{err}")
    return None, None, None
