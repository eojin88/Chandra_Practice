/**
 * 설치 명령어: npm install express multer axios cors
 */

const express = require('express');
const multer = require('multer');
const axios = require('axios');
const cors = require('cors');
const path = require('path');
const FormData = require('form-data');

const app = express();
const port = 3000;

// CORS 설정: 모든 도메인 허용
app.use(cors());
// JSON 파싱 설정
app.use(express.json());
// 정적 파일 서비스 (HTML, CSS, JS)
app.use(express.static('public'));

// Multer 설정: 메모리에 이미지 임시 저장
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

/**
 * 이미지 분석 요청을 FastAPI 서버로 전달하는 프록시 엔드포인트
 */
app.post('/proxy-analyze', upload.single('image'), async (req, res) => {
    try {
        const question = req.body.question;
        const imageFile = req.file;

        if (!imageFile) {
            return res.status(400).json({ success: false, message: "이미지 파일이 없습니다." });
        }

        // FastAPI 서버로 보낼 폼 데이터 구성
        const formData = new FormData();
        formData.append('image', imageFile.buffer, {
            filename: imageFile.originalname,
            contentType: imageFile.mimetype,
        });
        formData.append('question', question);

        // FastAPI 서버 (http://localhost:8000/analyze)로 요청 전달
        const response = await axios.post('http://localhost:8000/analyze', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        // 성공 결과 반환
        res.json(response.data);

    } catch (error) {
        // 예외 발생 시 에러 메시지 반환
        console.error("Error during analysis:", error.message);
        res.status(500).json({ 
            success: false, 
            message: "AI 서버 통신 중 오류가 발생했습니다: " + error.message 
        });
    }
});

/**
 * 서버 실행
 */
app.listen(port, () => {
    console.log(`서버가 구동되었습니다: http://localhost:${port}`);
});
