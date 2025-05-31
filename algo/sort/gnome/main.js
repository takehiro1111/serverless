const gnomeSort = numbers => {
  const lenNumbers = numbers.length
  let index = 0

  while (index < lenNumbers) {
    if(index === 0) {
      index ++
    }

    if (numbers[index] >= numbers[index - 1]) {
      index++;
    } else if (numbers[index] < numbers[index-1]) {
      [numbers[index - 1], numbers[index]] = [numbers[index], numbers[index - 1]];
      index--;
    }
  }

  return numbers
}

const numbers = Array.from({length: 10}, () =>
  Math.floor(Math.random() * 100)
)

console.log(gnomeSort(numbers))
