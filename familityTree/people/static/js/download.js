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

function createSvg(width, height) {
    var original = d3.select('#svg').node();
    var div = d3.select('body')
                .append('div')
                .attr('id', 'output-svg')
                .style('display', 'none')
                .html(original.innerHTML)
                .node()
    var svg = d3.select('#output-svg svg')
                .attr('version', 1.1)
                .attr('xmlns', 'http://www.w3.org/2000/svg')
                .attr('width', width)
                .attr('height', height)
                .node();

    //コピーしたsvgから全てのエレメントを取り出す
    var allElements = traverse(svg);
    var i = allElements.length;
    while (i--) {
        explicitlySetStyle(allElements[i]); //エレメントにcss -> atributeの変換を適用する
    }
    var html = svg.parentNode.innerHTML.replace(/\NS\d*:/gi, '');
    html = html.replace(/transform=".*?"/, '');
    var start = '<svg';
    var end = '</svg>';
    html = html.slice(html.indexOf(start), html.indexOf(end) + end.length);
    html = html.replace(/[^\x00-\x7f]/g, function(x) {
      return '&#' + x.charCodeAt(0) + ';';
    });
    div.remove();
    return 'data:image/svg+xml;base64,' + btoa(html, true);
}

function exportSvg(width, height) {
    var imgsrc = createSvg(width, height);
    var source = 'data:text/html;charset=utf-8,' + encodeURI('<html><head></head><body><p><img style="width:' + width + 'px; height: ' + height + 'px;" src="' + imgsrc + '"></p></body>');
    var a = d3.select('body').append('a');
    a.attr('class', 'downloadLink')
     .attr('download', 'chart.svg')
     .attr('target', '_blank')
     .attr('href', source)
     .text('test')
     .style('display', 'none')
    a.node().click();
    setTimeout(function() {
        a.remove();
    }, 10);
}

function exportPng(width, height) {
    var imgsrc = createSvg(width, height);
    var canvas = d3.select('body').append('canvas');
    canvas.style('display', 'none')
          .attr('id', 'canvas1')
          .attr('width', width)
          .attr('height', height)
    var ctx = canvas.node().getContext('2d');
    var image = new Image();
    image.onload = function() {
        ctx.drawImage(image, 0, 0);
        var source = 'data:text/html;charset=utf-8,' + encodeURI('<html><head></head><body><p><img style="width:' + width + 'px; height: ' + height + 'px;" src="' + canvas.node().toDataURL('image/png') + '"></p></body>');
        var a = d3.select('body').append('a');
        a.attr('class', 'downloadLink')
         .attr('download', 'chart.png')
         .attr('target', '_blank')
         .attr('href', source)
         .text('download png')
         .style('display', 'none')
        a.node().click();
    }
    image.src = imgsrc;
}
