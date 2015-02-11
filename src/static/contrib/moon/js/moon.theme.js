


// 根据比例数值（0-1）返回相应的红色到绿色的渐变色
function colorProportion(proportion) {
    // 0% rgb(153,0,0)
    // 50% rgb(153,204,0)
    // 100% rgb(0,153,0)
    var red = parseInt(proportion > .5 ? 153*(1 - proportion)*2 : 153);
    var green = parseInt(proportion > .5 ? 204 + 51*(1 - proportion*2) : 204*proportion*2);
    return 'rgb(' + red + ',' + green + ',0)';
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
