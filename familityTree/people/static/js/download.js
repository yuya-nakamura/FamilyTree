var target_style = ["font-size", "stroke", "fill", "stroke-width", "display", "opacity"];

function traverse(obj){
    var tree = [];
    tree.push(obj);
    visit(obj);
    function visit(node) {
        if (node && node.hasChildNodes()) {
            var child = node.firstChild
            while (child) {
                if (child.nodeType === 1 && child.nodeName != 'SCRIPT') {
                    tree.push(child);
                    visit(child);
                }
                child = child.nextSibling;
            }
        }
    }
    return tree;
}

function explicitlySetStyle(element) {
    var cSSStyleDeclarationComputed = getComputedStyle(element);
    var attributes = Object.keys(element.attributes).map(function(i) { return element.attributes[i].name; } );
    var i, len;
    var computedStyleStr = "";
    for (i = 0, len=cSSStyleDeclarationComputed.length; i < len; i++) {
        var key=cSSStyleDeclarationComputed[i];
        var value=cSSStyleDeclarationComputed.getPropertyValue(key);
        if(!attributes.some(function(k){ return k === key}) && target_style.indexOf(key) !== -1) {
            computedStyleStr += key + ":" + value + ";";
        }
    }
    element.setAttribute('style', computedStyleStr);
}

function exportSvg() {
    var svg = d3.select('svg').attr('version', 1.1).attr('xmlns', 'http://www.w3.org/2000/svg').node();

    //コピーしたsvgから全てのエレメントを取り出す
    var allElements = traverse(svg);
    var i = allElements.length;
    while (i--) {
        explicitlySetStyle(allElements[i]); //エレメントにcss -> atributeの変換を適用する
    }
    var html = svg.parentNode.innerHTML.replace(/\NS\d*:/g, '');
    html = html.replace('<br class=\"clear\">', '');
    html = html.replace(/[^\x00-\x7f]/g, function(x) {
      return '&#' + x.charCodeAt(0) + ';';
    });
    var imgsrc = 'data:image/svg+xml;base64,' + btoa(html, true);
    var source = 'data:text/html;charset=utf-8,' + encodeURI('<html><head></head><body><p><img style="width: 100vw; height: 100vh;" src="' + imgsrc + '"></p></body>');
    var a = d3.select('body').append('a');
    a.attr('class', 'downloadLink')
     .attr('download', 'chart.svg')
     .attr('href', source)
     .text('test')
     .style('display', 'none')
    a.node().click();
}
