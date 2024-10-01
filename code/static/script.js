document.addEventListener('DOMContentLoaded', function() {
    let socket;
    const statusDiv = document.getElementById('status');
    const reconnectButton = document.getElementById('reconnect');

    // Инициализация графика Plotly
    const layout = {
        xaxis: { title: 'X', range: [-10, 110] },
        yaxis: { title: 'Y', range: [-10, 110] }
    };
        const data = [
        {
            x: [],
            y: [],
            mode: 'markers',
            type: 'scatter',
            name: 'source1',
            text: [], // Для всплывающих подсказок
            hoverinfo: 'text', // Указываем, что показывать в подсказке
            marker: { size: 10, color: 'red' }
        },
        {
            x: [],
            y: [],
            mode: 'markers',
            type: 'scatter',
            name: 'source2',
            text: [], // Для всплывающих подсказок
            hoverinfo: 'text',
            marker: { size: 10, color: 'blue' }
        },
        {
            x: [],
            y: [],
            mode: 'markers',
            type: 'scatter',
            name: 'source3',
            text: [], // Для всплывающих подсказок
            hoverinfo: 'text',
            marker: { size: 10, color: 'green' }
        }
    ];

    // Проверка загрузки Plotly
    if(typeof Plotly !== 'undefined') {
        console.log("Plotly is loaded");
        Plotly.newPlot('graph', data, layout);
    } else {
        console.error("Plotly is not loaded");
    }

    function connect() {
        console.log("Attempting to connect...");
        socket = new WebSocket('ws://' + window.location.host + '/ws');

        socket.onopen = function(event) {
            console.log("Соединение установлено");
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log("Получено сообщение:", data);
            updateGraph(data);
        };
    }

    function updateGraph(data) {
        const traceIndex = data.sourceId === 'source1' ? 0 : (data.sourceId === 'source2' ? 1 : 2);

        const hoverText = `ID: ${data.id.slice(-4)}<br>Source: ${data.sourceId}<br>receivedAt: ${data.receivedAt}`;

        Plotly.extendTraces('graph', {
            x: [[data.x]],
            y: [[data.y]],
            text: [[hoverText]]
        }, [traceIndex]);

        // Обновляем аннотацию
        // const annotations = [{
        //     x: data.x,
        //     y: data.y,
        //     text: `ID: ${data.id}<br>Source: ${data.sourceId}<br>Time: ${new Date(data.receivedAt).toLocaleTimeString()}`,
        //     // showarrow: true,
        //     // arrowhead: 4,
        //     // arrowsize: 1,
        //     // arrowwidth: 2,
        //     // ax: 0,
        //     // ay: -40
        // }];

        Plotly.relayout('graph', {
        'xaxis.title': 'X',
        'xaxis.range': [-20, 120],  // Добавляем небольшой отступ
        'yaxis.title': 'Y',
        'yaxis.range': [-20, 120],
        'width': 600,
        'height': 600
});
    }

    if (reconnectButton) {
        reconnectButton.addEventListener('click', connect);
    } else {
        console.error("Element with id 'reconnect' not found");
    }

    connect();
});