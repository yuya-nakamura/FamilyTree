window.onload = function () {
    var g = new dagreD3.graphlib.Graph().setGraph({});

    // topレベルはdisplay:none
    g.setNode('top', {
        label: '',
        style: 'display: none;'
    });

    g.setNode('祖父', {
        label: '祖父'
    });
    // 結婚関係はdisplay:none
    g.setNode('祖父母', {
        label: '',
        style: 'display: none;'
    });
    g.setNode('祖母', {
        label: '祖母'
    });

    g.setNode('父兄', {
        label: '父兄'
    });
    g.setNode('父', {
        label: '父'
    });
    // 結婚関係はdisplay:none
    g.setNode('父母', {
        label: '',
        style: 'display:none;'
    });
    g.setNode('母', {
        label: '母'
    });
    g.setNode('父弟', {
        label: '父弟'
    });

    g.setNode('自分', {
        label: '自分'
    })
    g.setNode('弟', {
        label: '弟'
    });

    g.setEdge('父母', '自分', {
        arrowhead: 'undirected',
        // style: 'display:none;'
    });
    g.setEdge('父母', '弟', {
        arrowhead: 'undirected',
        // style: 'display:none;'
    });

    g.setEdge('祖父母', '父兄', {
        arrowhead: 'undirected',
        // style: 'display:none;'
    });
    g.setEdge('祖父母', '父', {
        arrowhead: 'undirected',
        // style: 'display:none;'
    });
    // 結婚関係同士はdisplay:none
    g.setEdge('祖父母', '父母', {
        arrowhead: 'undirected',
        style: 'display:none;',
    });
    // 兄弟以外の配偶者はdisplay:none
    g.setEdge('祖父母', '母', {
        arrowhead: 'undirected',
        style: 'display:none;'
    });
    g.setEdge('祖父母', '父弟', {
        arrowhead: 'undirected',
        // style: 'display:none;'
    });

    // topと関連するのはdisplay:none
    g.setEdge('top', '祖父', {
        arrowhead: 'undirected',
        style: 'display:none;'
    });
    g.setEdge('top', '祖父母', {
        arrowhead: 'undirected',
        style: 'display:none;'
    });
    g.setEdge('top', '祖母', {
        arrowhead: 'undirected',
        style: 'display:none;'
    });

    var svg = d3.select('svg'),
        inner = svg.select('g');

    // Set up zoom support
    var zoom = d3.behavior.zoom().on('zoom', function () {
        inner.attr('transform', 'translate(' + d3.event.translate + ')' + 'scale(' + d3.event.scale + ')');
    });
    svg.call(zoom);

    //Create the renderer
    var render = new dagreD3.render();

    // Run the renderer. This is what draws the final graph.
    render(inner, g);

    // 婚姻関係を描画する
    var output = svg.select('g .output');
    var siblings = output.insert('g', 'g.nodes')
        .attr('class', 'siblings');
    siblings.append('path')
        .attr('class', 'sibling')
        .attr('d', sblingLine);

    function sblingLine(d, i) {
        var node1 = g.node('父');
        var node2 = g.node('母');
        var linedata = [{
            x: node1.x,
            y: node1.y
        }, {
            x: node2.x,
            y: node2.y
        }];
        var fun = d3.svg.line().x(function (d) {
            return d.x;
        }).y(function (d) {
            return d.y;
        }).interpolate('linear');
        return fun(linedata);
    }

    // Center the graph
    var initialScale = 1;
    zoom.translate([(window.innerWidth - g.graph().width * initialScale) / 2, 20])
        .scale(initialScale)
        .event(svg);
};