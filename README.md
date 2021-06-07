# Solution of challenge

See the **Instructions.md** file before to run this project.

# Backend Developer Challenge
This is a simple challenge to test your skills on building APIs and your logic.
It has to be done using Python and Django/Django Rest Framework

# What to do
Create a Rest API that controls a car maintenance status, and the trips it performs. Note that, each litre of gas can run 8 KM and every 3 KM the tyres degrades by 1%.


# Objects:
- Tyre
-- Should have its degradation status in %
- Car
-- Should have 4 tyres
-- Should have its total gas capacity in liter
-- Should have its current gas count in %

# Actions:
- Trip
-- Input: car, distance (in KM)
-- Output: Complete car status on trip end

- Refuel
-- Input: car, gas quantity (in Litre)
-- Output: Final car gas count in %

- Maintenance
-- Input: car, part to replace
-- Output: Complete car status

- CreateCar
-- Input: None
-- Output: Complete car status

- GetCarStatus
-- Input: car
-- Output: Complete car status

- CreateTyre
-- Input: car
-- Output: The created tyre

# Restrictions:
- The car should **NOT** have more than 4 tyres in use
- The car should **NOT** be refueled before it has less than 5% gas on tank
- A car's tyre should **NOT** be swapped before it hits more than 94% degradation
- A tyre should **NOT** be created while there is 4 usable tyres with less than 95% degradation
- The car **cannot** travel without gas or one of its tyres

# Challenge
- Write an algorithm in the form of UnitTest that runs a trip of 10.000 KM, without breaking any part or swapping cars or gets out of gas.
- Document your project, with instructions on how to setup and run a working example.

# Recommendations
- SOLID / DRY
- Code and Commits in english (methods, classes, variables, etc)

# Evaluation
- Project Structure, architecturing and organization
- Logic
- VCS Practices

# Delivery
You must **fork** this repository and commit the solution in the **solution** folder. Your repository must be **public**. After that, sand the repository link by email to **giovani.souza@pland.com.br**
