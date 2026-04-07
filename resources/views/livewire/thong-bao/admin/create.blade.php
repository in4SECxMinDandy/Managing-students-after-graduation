<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Gửi thông báo</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <form wire:submit="send" class="max-w-lg bg-white p-6 rounded-lg shadow space-y-4">
        <div>
            <label class="block text-gray-700 font-medium mb-2">Nội dung thông báo</label>
            <textarea wire:model="noiDung" rows="4"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập nội dung..."></textarea>
            @error('noiDung') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div>
            <label class="block text-gray-700 font-medium mb-2">Gửi đến</label>
            <select wire:model.live="loai"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="all">Tất cả sinh viên</option>
                <option value="khoa">Theo Khoa</option>
                <option value="nganh">Theo Ngành</option>
                <option value="lop">Theo Lớp</option>
            </select>
        </div>

        @if ($loai === 'khoa')
            <div>
                <label class="block text-gray-700 font-medium mb-2">Khoa</label>
                <select wire:model="maKhoa"
                    class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">-- Chọn khoa --</option>
                    @foreach ($khoas as $khoa)
                        <option value="{{ $khoa['ma_khoa'] }}">{{ $khoa['ten_khoa'] }}</option>
                    @endforeach
                </select>
            </div>
        @endif

        <button type="submit"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 font-medium">
            Gửi thông báo
        </button>
    </form>
</div>
