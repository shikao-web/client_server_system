document.getElementById("contactForm").addEventListener("submit", function (e) {
    e.preventDefault(); // ページリロード防止

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    // 簡単なバリデーション
    if (!name || !email || !message) {
        document.getElementById("result").textContent = "全て入力してください";
        return;
    }

    // 擬似送信（本当はサーバーに送る）
    console.log({ name, email, message });

    document.getElementById("result").textContent = "送信しました！";

    // フォームリセット
    document.getElementById("contactForm").reset();
});