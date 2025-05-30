const selectionSort = (numbers) => {
  console.log("初期配列:", numbers);

  if (Array.isArray(numbers)) {
    for (let i = 0; i < numbers.length; i++) {
      let minIdx = i;
      console.log(`\n--- 外側ループ idx:${i} ---`);
      console.log(`初期minIdx: ${minIdx}, 値: ${numbers[minIdx]}`);

      console.log(`\n--- 内側ループ idx:${i} ---`);
      for (let j = i + 1; j < numbers.length; j++) {
        console.log(`比較: numbers[${minIdx}] (${numbers[minIdx]}) vs numbers[${j}] (${numbers[j]})`);
        // 最小値のインデックスを探す
        if (numbers[minIdx] > numbers[j]) {
          // 最終的に最小値の要素を持つインデックスが入る。
          console.log(`現在のminIdx: ${minIdx}`);
          minIdx = j;
          console.log(`新しいminIdx: ${minIdx}`);
        }
      }
      // 内側ループ完了後に一度だけスワップ(入れ替える。)
      // ループの時点でのインデックスに最小値を持ってくる。
      console.log(`スワップ前: [${numbers[i]}, ${numbers[minIdx]}]`);
      [numbers[i], numbers[minIdx]] = [numbers[minIdx], numbers[i]];
      console.log(`スワップ後の配列:`, numbers);
    }

    return numbers;
  }
};

const numbers = Array.from({ length: 10 }, () =>
  Math.floor(Math.random() * 1000)
);
console.log(selectionSort(numbers));
