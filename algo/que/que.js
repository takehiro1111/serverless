class Queue {
  constructor(){
    this.que = []
  }

  get getQueue() {
    return this.que
  }

  enqueue(data) {
    this.que.push(data)
  }

  dequeue() {
    if (this.que.length > 0){
      return this.que.shift()
    }
    return undefined
  }

  reverseQueue(arr){
    const newQue = []

    const tempArr = [...arr];
    while (tempArr.length > 0) {
      newQue.push(tempArr.pop());
    }
    return newQue;
  }
}

const q = new Queue()
q.enqueue(1);
q.enqueue(2);
q.enqueue(3);

console.log(q.getQueue); // [1, 2, 3]

console.log(q.dequeue()); // 1
console.log(q.dequeue()); // 2
console.log(q.getQueue); // [2, 3]

const originalArray = [5, 6, 7, 8];
const reversedArray = q.reverseQueue(originalArray);
console.log(reversedArray); // [8, 7, 6, 5]
console.log(originalArray); // [5, 6, 7, 8] (元の配列は変更されない)
