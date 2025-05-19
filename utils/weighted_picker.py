import random


class WeightedPicker():
	def __init__(self, input_weights, weight_key='weight'):
		self.input_weights = input_weights
		self.weight_key = weight_key
		self._weight_totals = None

	@property
	def weight_totals(self):
		if not self._weight_totals:
			self._weight_totals = self._generate_weight_list()
		return self._weight_totals

        def _build_weight_totals(self):
                # Example implementation; yours may differ
                totals = []
                running_total = 0
                for item in self.input_weights:
                        running_total += getattr(item, self.weight_key, 1)
                        totals.append(running_total)
                return totals
	
	def next(self):
                if not self.input_weights:
                        raise ValueError("WeightedPicker: No items to pick from.")
                if self._weight_totals is None:
                        self._weight_totals = self._build_weight_totals()
                if not self._weight_totals:
                        raise ValueError("WeightedPicker: No weights to pick from.")
		weight_total_count = len(self._weight_totals)
		target_number = random.randint(0, self._weight_totals[-1] - 1)
		mid_level = 0
		min_level = 0
		max_level = weight_total_count - 1

		if max_level == 0:
			return self._weight_totals[0]

		found = False
		while min_level <= max_level and not found:
			mid_level = round((min_level + max_level) / 2)
			if weight_total_count >= mid_level:
				this_value = self._weight_totals[mid_level]
				if target_number == this_value:
					found = True
					continue

				lower_value = 0
				if mid_level > 0:
					lower_value = self._weight_totals[mid_level - 1]

				if target_number > lower_value and target_number < this_value:
					found = True
					continue

				if target_number < this_value:
					max_level = mid_level - 1
				elif target_number > this_value:
					min_level = mid_level + 1
				else:
					# This should not happen
					target_number = random.randint(0, self._weight_totals[-1] - 1)
					mid_level = 0
					min_level = 0
					max_level = weight_total_count - 1

			else:
				# Start over
				target_number = random.randint(0, self._weight_totals[-1] - 1)
				mid_level = 0
				min_level = 0
				max_level = weight_total_count - 1

		return self.input_weights[mid_level]


	def _generate_weight_list(self):
		running_total = 0
		totals = []
		for item in self.input_weights:
			weight = item.get(self.weight_key, 1)
			running_total += weight
			totals.append(running_total)
		return totals

