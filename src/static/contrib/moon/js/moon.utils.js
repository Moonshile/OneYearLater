
// binary search for sorted arrays in range [lo, hi)
function binSearch(arr, lo, hi, target, cmp) {
    while(lo < hi) {
        var mi = (lo + hi) >> 1;
        if(cmp(target, arr[mi]) < 0) {
            hi = mi;
        } else {
            lo = mi + 1;
        }
    }
    return --lo;
}

function binSearchInArr(arr, target, cmp) {
    return binSearch(arr, 0, arr.length, target, cmp);
}
