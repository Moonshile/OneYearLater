
/*
 * js插件，显示水平长条状的历史数据
 * ele: jquery 选择器产生的对象
 * data: 形如 [{'weight': 2, 'color': '#f00'}, {'weight': 1, 'color': '#0f0'}]
 */
function historyHorizontal(ele, data) {
    var total = data.reduce(function(res, x) {
        return res + x.weight;
    }, 0);
    var percents = data.map(function(x) {
        return {'w': x.weight/total, 'c': x.color};
    });
    for(var i in percents){
        ele.append('<span style="width:' 
            + percents[i].w*100 
            + '%;border-color:' 
            + percents[i].c
            + ';">');
    }
}
