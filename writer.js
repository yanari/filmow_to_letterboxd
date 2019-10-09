const fs = require('fs');

module.exports.writeToCsv = (movie, fileNumber) => {
  fs.appendFileSync(`./file${fileNumber}.csv`, movie + '\n', (err) => {
    console.log(err);
  })
}
