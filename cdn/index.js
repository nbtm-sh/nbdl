const express = require("express");
const cfg = require("./config.json");
const mysql = require("mysql");

var app = express();

var con = mysql.createConnection({
  host: cfg.sql.host,
  user: cfg.sql.user,
  password: cfg.sql.password,
  database: cfg.sql.database
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

app.get("/*", function(req, res) {
    console.log(req.url.replace("/", "").split(".")[0]);
    con.query(`SELECT * FROM \`urls\` WHERE \`contentId\`="${req.url.replace("/", "").split(".")[0]}"`, function (err, result, fields, app_res=res) {
        if (err) throw err;
        if (result.length > 0) {
          res.sendFile(result[0]["contentFileName"]);
        } else {
          res.statusCode = 404; // Not found
          res.send("<html><span>404 Not Found</span></html>");
        }
      });
})

app.listen(3000);