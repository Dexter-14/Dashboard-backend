const express = require('express');
const cors = require('cors');
const fs = require('fs');
const readline = require('readline');
const app = express();
const path = require('path');

app.use(cors());
app.use(express.json());

app.get('/file', (req, res) => {
    const filePath = 'chandrap/all-metrics_chandrap.txt'; // Specify the path to your file
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Error reading the file' });
        }

        res.send(data);
    });
});

app.get('/files', (req, res) => {
    const folderPath = 'chandrap'; // Specify the path to your folder
    const fileNames = fs.readdirSync(folderPath);
    const fileData = [];

    fileNames.forEach((fileName) => {
      if (fileName !== 'all-metrics_chandrap.txt' && fileName !== 'chandrap_cjud.txt' && fileName !== 'chandraprmv123.txt') {
        const filePath = path.join(folderPath, fileName);
        const fileContent = fs.readFileSync(filePath, 'utf8');
        fileData.push({ filename: fileName, content: fileContent });
      }
    });

    res.json(fileData);
  });


  app.get('/loc-metrics', (req, res) => {
    const filePath = 'loc_chandrap/chandrap/LoC-metrics.txt'; // Specify the path to your Loc-metrics file
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        console.error(err);
        return res.status(500).json({ message: 'Error reading the file' });
      }

      res.send(data);
    });
  });


const port = 3001;

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});




// const express = require('express');
// const cors = require('cors');
// const fs = require('fs');
// const path = require('path');
// const { NodeSSH } = require('node-ssh'); // Require the SSH module

// const app = express();

// app.use(cors());
// app.use(express.json());

// // Function to execute a shell script using SSH
// async function executeShellScript(ssh, filePath) {
//   // const result = await ssh.execCommand(`bash ${filePath}`);
//   const result = await ssh.exec(filePath, [], {
//     onStdout(chunk) {
//       process.stdout.write(chunk.toString());
//     },
//     onStderr(chunk) {
//       process.stderr.write(chunk.toString());
//     }
//   });

//   if (result.code === 0) {
//     console.log(`Shell script ${filePath} executed successfully`);
//     // const fileDownResult = await ssh.exec('scp -r daagarwa@bgl-ads-6382:/nobackup/daagarwa/s1/daagarwa .');
//     // scp -r /nobackup/daagarwa/s1/daagarwa cisco\daagarwa@172.16.129.223:C:\Users\daagarwa\new_dash\Backend1
//     const fileDownResult = await ssh.exec('scp -r /nobackup/daagarwa/s1/daagarwa cisco/daagarwa@172.16.129.223:C:/Users/daagarwa/new_dash/Backend1');

//     if (fileDownResult.code === 0) {
//       console.log(`Shell script ${filePath} executed successfully`);

//     } else {
//       console.error(`Error executing shell script ${filePath}: ${fileDownResult.stderr}`);
//     }
//   } else {
//     console.error(`Error executing shell script ${filePath}: ${result.stderr}`);
//   }
// }

// app.get('/file', (req, res) => {
//   const filePath = 'chandrap/all-metrics_chandrap.txt'; // Specify the path to your file
//   fs.readFile(filePath, 'utf8', (err, data) => {
//     if (err) {
//       console.error(err);
//       return res.status(500).json({ message: 'Error reading the file' });
//     }

//     res.send(data);
//   });
// });

// app.get('/files', (req, res) => {
//   const folderPath = 'chandrap'; // Specify the path to your folder
//   const fileNames = fs.readdirSync(folderPath);
//   const fileData = [];

//   fileNames.forEach((fileName) => {
//     if (fileName !== 'all-metrics_chandrap.txt' && fileName !== 'chandrap_cjud.txt' && fileName !== 'chandraprmv123.txt') {
//       const filePath = path.join(folderPath, fileName);
//       const fileContent = fs.readFileSync(filePath, 'utf8');
//       fileData.push({ filename: fileName, content: fileContent });
//     }
//   });

//   res.json(fileData);
// });


// app.get('/loc-metrics', (req, res) => {
//   const filePath = 'loc_chandrap/chandrap/LoC-metrics.txt'; // Specify the path to your Loc-metrics file
//   fs.readFile(filePath, 'utf8', (err, data) => {
//     if (err) {
//       console.error(err);
//       return res.status(500).json({ message: 'Error reading the file' });
//     }

//     res.send(data);
//   });
// });

// const port = 3001;

// // Execute shell scripts when the app starts
// (async () => {
//   const ssh = new NodeSSH();

//   try {
//     console.log("trying to connect");
//     await ssh.connect({
//       host: 'bgl-ads-6382',
//       username: 'daagarwa',
//       password: 'Skrd@1234'
//     });
//     console.log("connected to server")
//     const shellScript1 = '/nobackup/daagarwa/individual_rmv_cjud_fw_1_to_6.sh daagarwa';
//     const shellScript2 = '/nobackup/daagarwa/individual_loc_generator.sh';

//     await executeShellScript(ssh, shellScript1);
//     // await executeShellScript(ssh, shellScript2);

//     app.listen(port, () => {
//       console.log(`Server is running on port ${port}`);
//     });
//   } catch (error) {
//     console.error(error);
//     ssh.dispose();
//   }
// })();


