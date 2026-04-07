<div class="text-center">
    <h2 class="text-2xl font-bold text-gray-800">Trang quản trị QLSVSDH</h2>
    <p class="mt-2 text-gray-600">Xin chào, {{ $admin->TenDN ?? 'Admin' }}</p>

    <div class="mt-8 grid grid-cols-2 md:grid-cols-3 gap-4">
        <a href="{{ route('admin.khoa') }}" class="p-4 bg-blue-100 rounded-lg hover:bg-blue-200">
            <div class="text-lg font-semibold">Khoa</div>
            <div class="text-sm text-gray-600">Quản lý Khoa</div>
        </a>
        <a href="{{ route('admin.nganh') }}" class="p-4 bg-green-100 rounded-lg hover:bg-green-200">
            <div class="text-lg font-semibold">Ngành</div>
            <div class="text-sm text-gray-600">Quản lý Ngành</div>
        </a>
        <a href="{{ route('admin.tuyen-sinh') }}" class="p-4 bg-purple-100 rounded-lg hover:bg-purple-200">
            <div class="text-lg font-semibold">Xét tuyển</div>
            <div class="text-sm text-gray-600">Duyệt hồ sơ</div>
        </a>
    </div>
</div>
