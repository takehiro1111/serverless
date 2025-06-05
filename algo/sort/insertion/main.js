const insertionSort = (numbers) => {
  const lenNumbers = numbers.length

  for(let i = 1; i < lenNumbers; i++) {
    let temp = numbers[i]

    let j = i -1

    while(j >= 0 && numbers[j] > temp) {
      numbers[j+1] = numbers[j]
      j -= 1
    }
    numbers[j+1] = temp
  }

  return numbers
}

console.log(insertionSort([1,5,4,3,2]))
