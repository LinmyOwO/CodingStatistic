SAVE_AMOUNT = 25


class DataHandler:
    def handle_result(self, data, number, time):
        if number in data:
            num_stat = data[number]

            num_stat['frequency'] += 1

            if len(num_stat['times']) == SAVE_AMOUNT:
                num_stat['times'].pop(0)
                num_stat['times'].append(time)
            else:
                num_stat['times'].append(time)

            if time < num_stat['best_time']:
                num_stat['best_time'] = time

        else:
            data[number] = {
                'frequency': 1,
                'best_time': time,
                'times': [time]
            }

    def find_average(self, array):
        sum = .0
        for elem in array:
            sum += elem
        return sum / len(array)

    def get_array_with_distinct_elem_length(self, array, length):
        res = [elem for elem in array if len(elem) == length]
        return res
