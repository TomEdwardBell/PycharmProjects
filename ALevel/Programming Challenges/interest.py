def debt_calculation(initial, interest, repayment):
    debt = initial
    total_paid = 0

    interest /= 100
    repayment /= 100
    months = 0

    while debt != 0:
        months += 1
        # One month has progressed

        debt += debt * interest
        # Add interest

        if debt * repayment > 50:
            olddebt = debt
            debt -= debt * repayment
            total_paid += olddebt * repayment
            # If the amount that would be repayed is over 50
            # Take away that amount

        else:
            olddebt = debt
            debt -= 50
            if debt > 0:
                total_paid += 50
            else:
                total_paid += olddebt
                debt = 0
            # If it's more  than 50
            # Take away 50
            # If the new debt is less than 0
                # Then add the whole of the old debt to the total paid
                # And set the debt to 0

        if debt != int(debt * 100) / 100:
            debt = (int(debt * 100) + 1) / 100

        if total_paid != int(total_paid * 100) / 100:
            total_paid = (int(total_paid * 100) + 1) / 100
        # Rounds it to two decimal places

    return(total_paid)

print(debt_calculation(100, 10, 50))