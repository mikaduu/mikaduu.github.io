
//以下是菜单显示和消失函数
const menuContainer=document.querySelector('.menu-container')
const menuIcon = document.getElementById('menu-icon');
const menu = document.getElementById('menu');

// 为菜单图标添加点击事件
menuIcon.addEventListener('click', (event) => {
    menu.classList.toggle('active'); 
    menuContainer.classList.toggle('active'); // 添加此行以确保菜单容器的状态切换
    menuIcon.classList.toggle('active');
    // 阻止事件冒泡
    event.stopPropagation();
});

// 点击空白处隐藏菜单
document.addEventListener('click', (event) => {
    if (!menu.contains(event.target) && event.target !== menuIcon) {
        //menuIcon.classList.toggle('active');
        //menuContainer.classList.toggle('active');
        if (menu.classList.contains('active')) {
            menu.classList.remove('active');
            menuContainer.classList.remove('active');
            menuIcon.classList.remove('active');
        } 
    }
});



//菜单显示和消失函数结束


//以下是欢迎页图片切换函数
document.addEventListener("DOMContentLoaded", function() {
    const parallaxImages = document.querySelectorAll('.parallax img'); // 获取所有幻灯片的图片
    const indicatorsContainer = document.querySelector('.indicators'); // 获取指示器容器
    const dynamicText = document.querySelector('.dynamic-text');// 获取动态文本元素
    let currentImageIndex = 0; // 当前显示的图片索引

    const texts = [
        "Welcome\n to \n My Minecraft Community!", // 图片1的文本
        "Adventure", // 图片2的文本
        "Survive", // 图片3的文本
        "Construction", // 图片4的文本
        "Creation"  // 图片5的文本
    ];
    // 初始化指示器
    parallaxImages.forEach((img, index) => {
        const indicator = document.createElement('li'); // 创建指示器圆点
        indicator.addEventListener('click', () => {
            switchImages(index); // 点击指示器切换至对应图片
        });

        indicatorsContainer.appendChild(indicator); // 将指示器添加到容器中
    });

    // 初始化视差效果
    // window.addEventListener('scroll', function() {
    //     const scrollPosition = window.scrollY; // 当前滚动位置
    //     parallaxImages[currentImageIndex].style.transform = 'translateY(' + (scrollPosition * 0.8) + 'px)'; // 视差效果
    // });

    // 图片切换函数
    function switchImages(index) {
        parallaxImages[currentImageIndex].style.opacity = 0; // 淡出当前图片
        indicatorsContainer.children[currentImageIndex].classList.remove('active'); // 更新指示器状态

        currentImageIndex = index; // 更新当前索引
        parallaxImages[currentImageIndex].style.opacity = 1; // 淡入下一张图片
        indicatorsContainer.children[currentImageIndex].classList.add('active'); // 更新指示器状态

        dynamicText.textContent = texts[currentImageIndex]; // 根据当前索引更新文本
    }
    

    // 设置定时切换图片
    setInterval(() => {
        switchImages((currentImageIndex + 1) % parallaxImages.length); // 切换到下一张图片
    }, 10000);

    // 初始化第一个指示器为活动状态
    indicatorsContainer.children[currentImageIndex].classList.add('active');
    dynamicText.textContent = texts[currentImageIndex]; // 根据当前索引更新文本
});
//欢迎页图片切换函数结束




//页面关闭自动注销
window.addEventListener("beforeunload", function(event) {
    // 使用 fetch 发送请求注销用户
    navigator.sendBeacon("/logout");
    login_status = false; // 设置登录状态为 false
});


document.addEventListener("DOMContentLoaded", function () {
    const photoImages = document.querySelectorAll('.photo img');
    let currentPhotoIndex = 0;

    // 显示当前图片
    function displayPhoto(index) {
        photoImages.forEach((img, i) => {
            img.style.opacity = i === index ? 1 : 0; // 显示当前图片，淡出其他图片
        });
    }

    // 图片切换函数
    function switchPhotos(index) {
        currentPhotoIndex = index;
        if (currentPhotoIndex < 0) {
            currentPhotoIndex = photoImages.length - 1; // 循环到最后一张
        } else if (currentPhotoIndex >= photoImages.length) {
            currentPhotoIndex = 0; // 循环到第一张
        }
        displayPhoto(currentPhotoIndex);
    }

    // 左右箭头点击事件
    document.getElementById('left-arrow').addEventListener('click', () => {
        switchPhotos(currentPhotoIndex - 1);
    });

    document.getElementById('right-arrow').addEventListener('click', () => {
        switchPhotos(currentPhotoIndex + 1);
    });

    // 设置定时切换图片
    setInterval(() => {
        switchPhotos(currentPhotoIndex + 1); // 切换到下一张图片
    }, 5000); // 每5000ms切换一张图片

    // 显示第一个图片
    displayPhoto(currentPhotoIndex);
});









//rubbish


//废弃的在前端处理重定向的异步函数
//注册表单提交函数
// document.getElementById("registerForm").addEventListener('submit',  function(event) {
//     event.preventDefault(); // 阻止默认表单提交
//     const formData = new FormData(event.target);
//
//     fetch("/register", {
//         method: "POST",
//         body: formData,
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 1) {
//             login_status = true; // 设置登录状态为 true
//             alert(data.message);
//             window.location.herf='/'
//         } else {
//             alert(data.message); // 显示错误信息
//             window.location.herf='/register'
//         }
//     })
//     .catch(error => console.error('Error:', error));
// })
//
// //登录表单提交函数
// document.getElementById("loginForm").addEventListener('submit', function(event) {
//     event.preventDefault(); // 阻止默认表单提交
//     const formData = new FormData(event.target);
//
//     fetch("/login", {
//         method: "POST",
//         body: formData,
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 1) {
//             login_status = true; // 设置登录状态为 true
//             alert(data.message);
//             window.location.herf='/'
//         } else {
//             alert(data.message); // 显示错误信息
//             window.location.herf='/login'
//         }
//     })
//     .catch(error => console.error('Error:', error));
// })