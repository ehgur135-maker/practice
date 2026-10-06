
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="기사의 여행",
    page_icon="knight.png"
)

st.title("♞ 기사의 여행")

st.write(
    "기사를 직접 움직여 체스판의 모든 칸을 한 번씩 방문해 보세요."
)

n = st.selectbox(
    "체스판 크기",
    [5, 6, 7, 8],
    index=3
)

html = f"""
<!DOCTYPE html>

<html>

<head>

<style>

body {{
    font-family: sans-serif;
}}

#info {{
    text-align: center;
    font-size: 20px;
    margin: 15px;
}}

#board {{
    display: grid;
    grid-template-columns: repeat({n}, 70px);
    width: fit-content;
    margin: 30px auto;
    border: 4px solid #222;
}}

.cell {{
    width: 70px;
    height: 70px;

    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 35px;
    cursor: pointer;

    box-sizing: border-box;
}}

.light {{
    background-color: #f0d9b5;
}}

.dark {{
    background-color: #b58863;
}}

.possible {{
    background-color: #90ee90;
}}

.current {{
    background-color: #ffd700;
}}

.visited {{
    background-color: #9ec5fe;
}}

.number {{
    font-size: 18px;
    font-weight: bold;
}}

#message {{
    text-align: center;
    font-size: 18px;
    margin: 15px;
}}

#reset {{
    display: block;
    margin: 20px auto;
    padding: 10px 25px;

    font-size: 17px;
    font-weight: bold;

    border: none;
    border-radius: 8px;

    background-color: #555;
    color: white;

    cursor: pointer;
}}

#reset:hover {{
    background-color: #333;
}}

</style>

</head>


<body>

<div id="info">
    시작할 칸을 선택하세요.
</div>

<div id="board"></div>

<div id="message"></div>

<button id="reset" onclick="resetGame()">
    🔄 다시 시작
</button>


<script>

const n = {n};

const board = document.getElementById("board");

const info = document.getElementById("info");

const message = document.getElementById("message");


let currentRow = null;
let currentCol = null;

let path = [];


// ------------------------------------------------
// 기사 이동 규칙
// ------------------------------------------------

function isKnightMove(r, c) {{

    if (currentRow === null) {{
        return false;
    }}

    const dr = Math.abs(r - currentRow);
    const dc = Math.abs(c - currentCol);

    return (
        (dr === 2 && dc === 1) ||
        (dr === 1 && dc === 2)
    );
}}


// ------------------------------------------------
// 현재 위치에서 이동 가능한 칸 찾기
// ------------------------------------------------

function getPossibleMoves() {{

    const moves = [];

    for (let r = 0; r < n; r++) {{

        for (let c = 0; c < n; c++) {{

            const alreadyVisited = path.some(
                p => p[0] === r && p[1] === c
            );

            if (alreadyVisited) {{
                continue;
            }}

            if (isKnightMove(r, c)) {{
                moves.push([r, c]);
            }}
        }}
    }}

    return moves;
}}


// ------------------------------------------------
// 체스판 그리기
// ------------------------------------------------

function drawBoard() {{

    board.innerHTML = "";

    const possibleMoves = getPossibleMoves();

    for (let r = 0; r < n; r++) {{

        for (let c = 0; c < n; c++) {{

            const cell = document.createElement("div");

            cell.classList.add("cell");


            // 체스판 색
            if ((r + c) % 2 === 0) {{
                cell.classList.add("light");
            }}
            else {{
                cell.classList.add("dark");
            }}


            // 방문 순서
            const index = path.findIndex(
                p => p[0] === r && p[1] === c
            );


            // 방문했던 칸
            if (index !== -1) {{

                cell.classList.add("visited");

                const number = document.createElement("span");

                number.classList.add("number");

                number.textContent = index + 1;

                cell.appendChild(number);
            }}


            // 현재 위치
            if (
                r === currentRow &&
                c === currentCol
            ) {{

                cell.classList.add("current");

                cell.innerHTML = "♞";
            }}


            // 이동 가능한 칸
            const isPossible = possibleMoves.some(
                p => p[0] === r && p[1] === c
            );

            if (isPossible) {{

                cell.classList.add("possible");
            }}


            // 클릭
            cell.onclick = function() {{

                moveKnight(r, c);

            }};


            board.appendChild(cell);
        }}
    }}


    // 정보 표시
    if (currentRow === null) {{

        info.innerHTML =
            "시작할 칸을 선택하세요.";

    }}
    else {{

        info.innerHTML =
            "현재 위치: (" +
            (currentRow + 1) +
            ", " +
            (currentCol + 1) +
            ") &nbsp;&nbsp; | &nbsp;&nbsp;" +
            "이동 가능한 칸: <b>" +
            possibleMoves.length +
            "개</b>";

    }}
}}


// ------------------------------------------------
// 기사 이동
// ------------------------------------------------

function moveKnight(r, c) {{

    message.innerHTML = "";


    // 첫 번째 이동
    if (currentRow === null) {{

        currentRow = r;
        currentCol = c;

        path.push([r, c]);

        drawBoard();

        return;
    }}


    // 이미 방문한 칸
    const alreadyVisited = path.some(
        p => p[0] === r && p[1] === c
    );

    if (alreadyVisited) {{

        message.innerHTML =
            "❌ 이미 방문한 칸입니다.";

        return;
    }}


    // 기사 이동 규칙
    if (!isKnightMove(r, c)) {{

        message.innerHTML =
            "❌ 기사는 L자 모양으로 이동해야 합니다.";

        return;
    }}


    // 이동
    currentRow = r;
    currentCol = c;

    path.push([r, c]);

    drawBoard();


    // 모든 칸 방문
    if (path.length === n * n) {{

        info.innerHTML =
            "🎉 <b>성공!</b> 모든 칸을 방문했습니다!";

        message.innerHTML =
            "기사의 여행을 완성했습니다!";

        return;
    }}


    // 더 이상 이동할 수 없는 경우
    const possibleMoves = getPossibleMoves();

    if (possibleMoves.length === 0) {{

        message.innerHTML =
            "⚠️ 더 이상 이동할 수 있는 칸이 없습니다.";

    }}

}}


// ------------------------------------------------
// 다시 시작
// ------------------------------------------------

function resetGame() {{

    currentRow = null;
    currentCol = null;

    path = [];

    message.innerHTML = "";

    drawBoard();
}}


// ------------------------------------------------
// 처음 체스판 표시
// ------------------------------------------------

drawBoard();

</script>

</body>

</html>
"""

components.html(
    html,
    height=750
)
