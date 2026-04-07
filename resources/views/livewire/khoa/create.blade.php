<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Thêm Khoa mới</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <form wire:submit="save" class="max-w-md bg-white p-6 rounded-lg shadow">
        <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Mã Khoa</label>
            <input type="text" wire:model="maKhoa" maxlength="2"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('maKhoa') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2">Tên Khoa</label>
            <input type="text" wire:model="tenKhoa"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('tenKhoa') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div class="flex space-x-4">
            <button type="submit"
                class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 font-medium">
                Lưu
            </button>
            <a href="{{ route('admin.khoa') }}"
               class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 font-medium text-center">
                Hủy
            </a>
        </div>
    </form>
</div>
