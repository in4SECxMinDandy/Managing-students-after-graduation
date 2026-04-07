<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">
        Thông báo
        @if ($chuaDocCount > 0)
            <span class="bg-red-500 text-white text-sm px-2 py-1 rounded-full">{{ $chuaDocCount }} mới</span>
        @endif
    </h2>

    <div class="space-y-4">
        @forelse ($thongBaos as $item)
            <div class="bg-white p-4 rounded-lg shadow {{ !$item['trang_thai_doc'] ? 'border-l-4 border-blue-500' : '' }}">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="font-medium text-gray-800">{{ $item['thong_bao']['noi_dung'] }}</p>
                        <p class="text-sm text-gray-500 mt-1">
                            {{ $item['thong_bao']['ngay_gui'] }}
                            @if ($item['thong_bao']['quan_tri'])
                                — {{ $item['thong_bao']['quan_tri']['ten_dn'] }}
                            @endif
                        </p>
                    </div>
                    @if (!$item['trang_thai_doc'])
                        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Mới</span>
                    @endif
                </div>
            </div>
        @empty
            <div class="text-center text-gray-500 py-8">Không có thông báo nào.</div>
        @endforelse
    </div>
</div>
