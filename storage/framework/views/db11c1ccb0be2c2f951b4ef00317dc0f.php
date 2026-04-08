<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QLSVSDH - Quản lý Sinh viên Đại học</title>
    <?php echo app('Illuminate\Foundation\Vite')(['resources/css/app.css']); ?>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen flex items-center justify-center">
    <div class="text-center">
        <h1 class="text-5xl font-extrabold text-blue-900 mb-4">QLSVSDH</h1>
        <p class="text-xl text-gray-700 mb-8">Hệ thống Quản lý Sinh viên Đại học</p>
        <div class="flex flex-wrap justify-center gap-4">
            <a href="<?php echo e(route('candidate.login')); ?>"
               class="bg-blue-600 text-white px-8 py-3 rounded-xl hover:bg-blue-700 font-semibold shadow-lg transition">
                Thí sinh
            </a>
            <a href="<?php echo e(route('student.login')); ?>"
               class="bg-green-600 text-white px-8 py-3 rounded-xl hover:bg-green-700 font-semibold shadow-lg transition">
                Sinh viên
            </a>
            <a href="<?php echo e(route('admin.login')); ?>"
               class="bg-gray-800 text-white px-8 py-3 rounded-xl hover:bg-gray-900 font-semibold shadow-lg transition">
                Quản trị
            </a>
        </div>
    </div>
</body>
</html>
<?php /**PATH C:\Users\haqua\Documents\GitHub\QLSVSDH\resources\views/welcome.blade.php ENDPATH**/ ?>