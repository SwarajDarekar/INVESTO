const express = require('express')
const app = express()
const port = 3010
var request = require('request')
var multer = require('multer');
var upload = multer();
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended:true}));
app.use(express.static(__dirname + '/public'));
app.set('view engine', 'ejs');
app.use(upload.array());

let mData=""
let coinName= "bitcoin"
let mChart=""
let oChart=""
let cryptoList =""
let tData=""

 async function resData(coinName){ 
   var marketData = await new Promise((resolve, reject) => {
request('https://api.coingecko.com/api/v3/coins/'+coinName, function (error, response, body) {
  console.error('error:', error); // Print the error if one occurred
  console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
  console.log('body:',typeof body);
  mData= JSON.parse(body)
   resolve(mData)
});

 })

 if(marketData){
  
    var ohlcChart = await new Promise((resolve, reject) => {
      request('https://api.coingecko.com/api/v3/coins/'+coinName+'/ohlc?vs_currency=inr&days=7', function (error, response, body) {
        console.error('error:', error); // Print the error if one occurred
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:',typeof body);
        oChart= JSON.parse(body)
         resolve(mData)
   
   });
   
    })
   }

if(ohlcChart){
 var marketChart = await new Promise((resolve, reject) => {
  request('https://api.coingecko.com/api/v3/coins/'+coinName+'/market_chart?vs_currency=inr&days=30', function (error, response, body) {
    console.error('error:', error); // Print the error if one occurred
    console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
    console.log('body:',typeof body);
    mChart= JSON.parse(body)
     resolve(mData)
  });
  
   })
  }
  if(marketChart){
    var listChart = await new Promise((resolve, reject) => {
    request('https://api.coingecko.com/api/v3/search/trending', function (error, response, body) {
     console.error('error:', error); // Print the error if one occurred
     console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
     console.log('body:',typeof body);
     cryptoList = JSON.parse(body)
      resolve(mData)
     });
     
      })
     }
  //    if(listChart){
  //     var trending = await new Promise((resolve, reject) => {
  //     request('https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en', function (error, response, body) {
  //      console.error('error:', error); // Print the error if one occurred
  //      console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
  //      console.log('body:',typeof body);
  //      tData = JSON.parse(body)
  // console.log(tData);
  //       resolve(mData)
  //      });
       
  //       })
  //      }
}




app.get('/', async(req, res) => {
  
    await resData(coinName)
  res.render('index',{ mData,mChart,coinName,oChart,cryptoList,tData})
})

app.post('/', async(req, res) => {
   
    coinName = req.body.selectCoin;
    await resData(coinName)
    res.render('index',{ mData,mChart,coinName,oChart,cryptoList,tData})
})

app.listen(port, () => {
  console.log(`Example app listening on http://localhost:${port}`)
})