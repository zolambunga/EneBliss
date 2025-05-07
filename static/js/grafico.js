//Função para configuração socket do grafico

/*
const socket = new WebSocket("ws://127.0.0.1:8000/ws/medicoes/");

socket.onmessage = function(event)
{
   const dados = Json.parse(event.data);
   const labels = dados.map(item => item.data_hora);
   const energia = dados.map(item => item.energia);

   // Atualiza o gráfico
   graficoEnergia.data.labels = labels;
   graficoEnergia.data.datasets[0].data = energia;
   graficoEnergia.update()
};


//Função para do grafico


const ctx = document.getElementById('graficoEnergia').getContext('2d');
const graficoEnergia = new Chart(ctx,
{
    type: 'line',
    data:
    {
        labels: [], //Inicialmente
        datasets: [
        {
            label: 'Energia Consumida (kWh)',
            data: [], //Inicialmente
            borderColor: 'green',
            fill: false
        }]
    },
    options:
    {
        responsive: true,
        scales:
        {
            x:
            {
                title:
                {
                    display: true,
                    text: 'Hora'
                }
            }
            y:
            {
                title:
                {
                    display:true,
                    text: 'Energia (kWh)'
                }
            }
        }
    }
});
*/

// Simulando dados
const socket = new WebSocket("ws://127.0.0.1:8000/ws/medicoes/");

socket.onmessage = function(event)
{
   const dados = Json.parse(event.data);
   const labels = graficoEnergia.data.labels;
   const dataset = graficoEnergia.datasets[0];

   // Adicionar dados simulados ao grafico
   labels.push(dados.data_hora);
   dataset.data.push(dados.energia);

   graficoEnergia.update()
};


//Função para do grafico


const ctx = document.getElementById('graficoEnergia').getContext('2d');
const graficoEnergia = new Chart(ctx,
{
    type: 'line',
    data:
    {
        labels: [], //Inicialmente
        datasets: [
        {
            label: 'Energia Consumida (kWh)',
            data: [], //Inicialmente
            borderColor: 'green',
            fill: false
        }]
    },
    options:
    {
        responsive: true,
        scales:
        {
            x:
            {
                title:
                {
                    display: true,
                    text: 'Hora'
                }
            }
            y:
            {
                title:
                {
                    display:true,
                    text: 'Energia (kWh)'
                }
            }
        }
    }
});
