// Given an array consisting of n integers, find the contiguous subarray whose length is greater than or equal to k that has the maximum average value.
// And you need to output the maximum average value.
//
// Example:
// Input: {1,12,-5,-6,50,3}, k = 4
// Output: 12.75
//
// Explanation: when length is 5, maximum average value is 10.8, when length is 6, maximum
// average value is 9.16667. Thus return 12.75.
//
// Note:
// 1 &lt;= k &lt;= n &lt;= 10,000. Elements of the given array will be in range [-10,000, 10,000]. The
// answer with the calculation error less than 10^-5 will be accepted.


function findMaxAverage(arr: number[], n: number, k: number) {
  // Check if 'k' is valid
  if (k > n) return -1;

    //Initializing the max with the lowest range
  let maxAvg = -10000;
  let sum = 0;

  for (let i = 0; i < n; i++) {
    sum += arr[i];

    if (i >= k - 1) {
      let average = sum / k;
      if (maxAvg < average) {
        maxAvg = average;
      }

      sum -= arr[i - k + 1];
    }
  }

  return maxAvg;
}

// Driver code
let arr = [1, 12, -5, -6, 50, 3];
let k = 4;
let n = arr.length;

console.log("🚀 Max average value:", findMaxAverage(arr, n, k));
