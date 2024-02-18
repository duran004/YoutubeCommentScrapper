<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Models\Video;
class VideosController extends Controller
{
    
    public function save_video(Request $request)
    {
        try{
            $video = new Video();
            $video->title =  $request->title;
            $video->url =  $request->url;
            $video->save();
            return response()->json(['message' => 'Video saved successfully']);
        }catch(\Exception $e){
            return response()->json(['message' => 'Error saving video', 'error' => $e->getMessage()]);
        }
    }

    public function get_video(){
        try{
            $video = Video::orderBy('checked', 'asc')->first();
            $video->increment('checked');
            $video->checked_at = now();
            $video->save();
            return response()->json($video);    
        }catch(\Exception $e){
            return response()->json(['message' => 'Error getting video', 'error' => $e->getMessage()]);
        }
    }
}
