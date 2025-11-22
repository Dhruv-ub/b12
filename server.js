const express = require('express');
const multer = require('multer');
const csv = require('csv-parser');
const fs = require('fs');
const cors = require('cors');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(cors());
app.use(express.json());

let uploadHistory = [];

app.post('/upload', upload.single('file'), (req, res) => {
    const results = [];
    
    fs.createReadStream(req.file.path)
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            fs.unlinkSync(req.file.path);
            
            const avgTemp = (results.reduce((sum, row) => sum + parseFloat(row.Temperature), 0) / results.length).toFixed(2);
            const avgPressure = (results.reduce((sum, row) => sum + parseFloat(row.Pressure), 0) / results.length).toFixed(2);
            const avgConc = (results.reduce((sum, row) => sum + parseFloat(row.Concentration), 0) / results.length).toFixed(2);
            const maxPressure = Math.max(...results.map(row => parseFloat(row.Pressure))).toFixed(2);
            const minPressure = Math.min(...results.map(row => parseFloat(row.Pressure))).toFixed(2);
            
            uploadHistory.unshift({
                id: Date.now(),
                timestamp: new Date().toLocaleString(),
                itemCount: results.length,
                avgPressure: avgPressure,
                data: results,
                summary: {
                    avgTemp: avgTemp,
                    avgPressure: avgPressure,
                    avgConcentration: avgConc,
                    maxPressure: maxPressure,
                    minPressure: minPressure
                }
            });
            
            if (uploadHistory.length > 5) {
                uploadHistory.pop();
            }
            
            res.json({
                message: 'File uploaded successfully',
                data: results,
                summary: {
                    avgTemp,
                    avgPressure,
                    avgConc,
                    maxPressure,
                    minPressure
                }
            });
        });
});

app.get('/history', (req, res) => {
    const historySummary = uploadHistory.map(item => ({
        id: item.id,
        timestamp: item.timestamp,
        itemCount: item.itemCount,
        summary: item.summary
    }));
    res.json(historySummary);
});

app.get('/history/:id', (req, res) => {
    const historyItem = uploadHistory.find(item => item.id === parseInt(req.params.id));
    if (historyItem) {
        res.json(historyItem);
    } else {
        res.status(404).json({ error: 'History item not found' });
    }
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});