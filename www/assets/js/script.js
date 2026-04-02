console.log("準備完了(script.js)")

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

    // 送信 (fetch では、裏でHTTP通信するだけ。 = 「非同期通信」)
    fetch("/api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, message })  // ここでフォームのデータをWebサーバーで送信
    });

    document.getElementById("result").textContent = "送信しました！";

    // フォームリセット
    document.getElementById("contactForm").classList.add("hidden");

});