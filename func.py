
def pars_salary(salary: str) -> tuple:
    try:
        if salary:
            temp1 = salary.split(" – ")
            if len(temp1) == 2:
                min_salary = temp1[0]
                temp2 = temp1[1].split(" ")
                max_salary = f"{temp2[0]} {temp2[1]}"
                currency = temp2[2]
                return min_salary, max_salary, currency
            if len(temp1) == 1:
                temp2 = temp1[1].split(" ")
                if temp2[0] == "до":
                    min_salary = None
                    max_salary = f"{temp2[1]} {temp2[2]}"
                    currency = temp2[3]
                elif temp2[0] == "от":
                    min_salary = f"{temp2[1]} {temp2[2]}"
                    max_salary = None
                    currency = temp2[3]
                return min_salary, max_salary, currency
    except Exception as err:
        print(salary)
    return None, None, None
