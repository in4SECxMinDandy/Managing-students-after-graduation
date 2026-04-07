<nav class="bg-blue-900 text-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
            <div class="flex items-center space-x-8">
                <a href="{{ route('admin.dashboard') }}" class="font-bold text-lg">QLSVSDH - Quản trị</a>
                <div class="hidden md:flex space-x-4">
                    <a href="{{ route('admin.khoa') }}" class="px-3 py-2 rounded hover:bg-blue-800">Khoa</a>
                    <a href="{{ route('admin.nganh') }}" class="px-3 py-2 rounded hover:bg-blue-800">Ngành</a>
                    <a href="{{ route('admin.lop') }}" class="px-3 py-2 rounded hover:bg-blue-800">Lớp</a>
                    <a href="{{ route('admin.mon-hoc') }}" class="px-3 py-2 rounded hover:bg-blue-800">Môn học</a>
                    <a href="{{ route('admin.tuyen-sinh') }}" class="px-3 py-2 rounded hover:bg-blue-800">Xét tuyển</a>
                    <a href="{{ route('admin.sinh-vien') }}" class="px-3 py-2 rounded hover:bg-blue-800">Sinh viên</a>
                    <a href="{{ route('admin.hoc-tap') }}" class="px-3 py-2 rounded hover:bg-blue-800">Học tập</a>
                    <a href="{{ route('admin.tot-nghiep') }}" class="px-3 py-2 rounded hover:bg-blue-800">Tốt nghiệp</a>
                    <a href="{{ route('admin.thong-bao') }}" class="px-3 py-2 rounded hover:bg-blue-800">Thông báo</a>
                </div>
            </div>
            <div class="flex items-center">
                <form action="{{ route('logout') }}" method="POST">
                    @csrf
                    <button type="submit" class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-sm">
                        Đăng xuất
                    </button>
                </form>
            </div>
        </div>
    </div>
</nav>
