
// 依赖于 moon.utils.js

/*
 * 产生渐变色
 * proportion: 当前颜色位置，为一个比例值，范围0-1
 * anchors: 锚点，形如[{'p': 0, 'c': 0xff0000}, {'p': .5, 'c': 0xffff00}, {'p': 1, 'c': 0x00ff00}]
 *         注意p的值必须包含0和1，该数组会被排序
 */
function colorGradient(proportion, anchors) {
    function compare(a, b) {
        return a.p - b.p;
    }
    anchors.sort(compare);
    var index = binSearchInArr(anchors, {"p": proportion}, compare);
    if (index == anchors.length - 1 || anchors[index].p == proportion) {
        return '#' + int2color(anchors[index].c);
    }
    var dProp = (proportion - anchors[index].p)/(anchors[index + 1].p - anchors[index].p)
    function component(loc) {
        var startCompo = anchors[index].c>>loc&0xff;
        var endCompo = anchors[index + 1].c>>loc&0xff;
        return (startCompo + dProp*(endCompo - startCompo))<<loc;
    }
    return '#' + int2color(component(16) | component(8) | component(0));
}

// 根据比例数值（0-1）返回相应的红色到绿色的渐变色
function colorProportion(proportion) {
    // 0% rgb(153,0,0) #990000
    // 50% rgb(153,204,0) #99cc00
    // 100% rgb(0,153,0) #009900
    return colorGradient(proportion, 
        [{'p': 0, 'c': 0x990000}, {'p': .5, 'c': 0x99cc00}, {'p': 1, 'c': 0x009900}]);
}

/*
 * js插件，显示水平长条状的历史数据
 * ele: jquery 选择器产生的对象
 * data: 形如 [{'proportion': 2}, {'proportion': 1}]
 */
function historyHorizontal(ele, data) {
    // var total = data.reduce(function(res, x) {
    //     return res + x.weight;
    // }, 0);
    // var percents = data.map(function(x) {
    //     return {'c': colorProportion(x.weight/total)};
    // });
    for(var i in data){
        ele.append('<span style="width:' 
            + 100/data.length 
            + '%;border-color:' 
            + colorProportion(data[i].proportion)
            + ';">');
    }
}
