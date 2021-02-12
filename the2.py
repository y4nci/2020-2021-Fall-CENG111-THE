import random
from evaluator import *

data = get_data()


def new_move():
	M, N, D = data[0], data[1], data[2]
	K, LAMBDA, MU = data[3], data[4], data[5]
	universal_state = data[6]
	occupied_locations = [p[0] for p in universal_state]  # To avoid having 1 < individuals with the same coordinates.
	directions = ["F", "FR", "R", "BR", "B", "BL", "L", "FL"]
	probabilities_directions = [MU / 2, MU / 8, (1 - MU - MU ** 2) / 2, 2 * (MU ** 2) / 5, (MU ** 2) / 5,
								2 * (MU ** 2) / 5, (1 - MU - MU ** 2) / 2, MU / 8]
	coordinate_wise_directions = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1),
								(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]

	# coordinate_wise_directions is the list indicating what direction 0, 1, 2 etc. is.
	# Each index references its coordinate - wise direction, for instance 5th index is the 5th move, i.e (-y, +x).
	# The reason why it is twice the length it should be will be clear a couple of lines later.

	for P in universal_state:

		index = universal_state.index(P)
		x, y = P[0][0], P[0][1]
		last_move, mask_status, infection_status = P[1], P[2], P[3]
		directions_dict = {"F": last_move, "FR": last_move + 1, "R": last_move + 2, "BR": last_move + 3,
						"B": last_move + 4, "BL": last_move + 5, "L": last_move + 6, "FL": last_move + 7}

		# Here it is, since the directions such as forward (F) and backward left (BL) depends on the last_move value,
		# their last_move values will depend on it too. I found the relation between last_move and new directions,
		# but as you can see if last_move is numerically bigger than 0, some directions exceed the (0, 8) range which
		# our directions are in. Hence the doubled coordinate_wise_directions list.

		random_direction = random.choices(directions, weights=probabilities_directions)
		new_direction = directions_dict[random_direction[0]]
		new_cwd = coordinate_wise_directions[new_direction]
		new_coordinates = (x + new_cwd[0], y + new_cwd[1])
		if new_coordinates in occupied_locations or new_coordinates[0] not in range(N) or new_coordinates[
			1] not in range(M):
			# This block is to eliminate illegal moves, such as the moves out of the plane or to occupied coordinates.

			new_coordinates = (x, y)
			new_direction = last_move

		if new_direction > 7:  # Remember, we still have values in range (8, 16) as coordinate-wise directions.
			new_direction -= 8  # Well, no more.

		P = [new_coordinates, new_direction, mask_status, infection_status]  # New status of the individual.
		occupied_locations[index] = new_coordinates  # Updating occupied coordinates.
		universal_state[index] = P  # Putting the individual back to its place in universal_state.

	# All individuals -well, at least the lucky ones- have been located. Now it's contamination time.

	newly_infected = []

	# Since we have to update their infection status at the end of this time frame instead of updating them immediately,
	# we also have to keep record of them. I will use this list for that very purpose.

	for P in universal_state:

		indexP = universal_state.index(P)
		xP, yP = P[0][0], P[0][1]
		mask_statusP, infection_statusP = P[2], P[3]

		for i in universal_state[indexP + 1:]:

			indexi = universal_state.index(i)
			xi, yi = i[0][0], i[0][1]
			mask_statusi, infection_statusi = i[2], i[3]
			distance = ((xP - xi) ** 2 + (yP - yi) ** 2) ** 0.5

			if distance <= D and infection_statusi != infection_statusP:  # Required specifications for contamination.

				probability_infection = min([1, (K / (distance ** 2))])

				if mask_statusi == "masked": probability_infection /= LAMBDA

				if mask_statusP == "masked": probability_infection /= LAMBDA

				probabilities_infections = [probability_infection, 1 - probability_infection]
				new_infection_status = random.choices(["infected", "notinfected"], weights=probabilities_infections)[0]

				# I had stated that infection status of the individuals should be different than each other in the if
				# statement above, but I didn't specify which individual was infected and which one wasn't. I will use
				# two more if statements for that.

				if infection_statusi == "notinfected":

					if new_infection_status == "infected":

						newly_infected.append(indexi)  # Newly infected individuals belong here.

				elif infection_statusP == "notinfected":

					if new_infection_status == "infected":

						newly_infected.append(indexP)  # Newly infected individuals belong here.

	for ind in newly_infected:  # Now it's time to update their infection status.

		universal_state[ind][3] = "infected"

	data[6] = universal_state  # To restore the new universal_state.

	return universal_state
