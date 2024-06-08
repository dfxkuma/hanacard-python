async function fetchData(url) {
    const response = await fetch(url);
    return await response.json();
}

async function getRecent() {
    const recentList = document.getElementById('recentList');
    const data = await fetchData("/get_recent");

    alert(data);

    data['DATA']['USED_LIST'].forEach(item => {
        const li = document.createElement('li');
        const itemDiv = document.createElement('div');

        if (item.MC_IMG_PATH) {
            const imgDiv = document.createElement('div');
            const img = document.createElement('img');
            img.src = "https://m.hanacard.co.kr" + item.MC_IMG_PATH;
            imgDiv.appendChild(img);
            itemDiv.appendChild(imgDiv);
        }

        const textDiv = document.createElement('div');
        const textNode = document.createTextNode(
            `${item.MC_NM}\n${item.APR_SYS_PC_DTTI}\n${item.WC_APR_AM}원`
        );
        textDiv.appendChild(textNode);
        itemDiv.appendChild(textDiv);

        li.appendChild(itemDiv);
        recentList.appendChild(li);
    });
}

async function login() {
    const data = await fetchData("/login/app");
    alert(data);
}

async function authVerifyChk() {
    const data = await fetchData("/auth_verify");
    console.log(data);

    const verifyStatusCode = data['DATA']['AUTH_VERIFY_CODE'];

    switch (verifyStatusCode) {
        case '00':
            alert('인증 성공');
            break;
        case '99':
            alert('유효시간 초과');
            break;
        case '9999':
            alert('서버 오류');
            break;
        default:
            alert('알 수 없는 오류');
            break;
    }
}

async function openApp() {
    const data = await fetchData("/code/app");
    console.log(data);

    const payLoginCode = data['DATA']['EASN_LGN_CTF_ID'];
    const appScheme = `oneqpay://app_card_auth?intro=on&ch=W&tc=01&tid=${payLoginCode}`;
    window.location.href = appScheme;
}
