<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Comment;
use Illuminate\Support\Facades\Log;

class CommentsController extends Controller
{
    public function save_comments(Request $request)
    {
        try{
            $video_id= $request->video_id;
            $comments= $request->comments;         
            $comments= json_decode($comments,true);

            for($i=0; $i<count($comments); $i++){
                $comment = $comments[$i];

                $isSaved=Comment::create([
                    'video_id' => $video_id,
                    'comment' => $comment['comment'],
                    'time' => $comment['comment_time'],
                    'writer' => $comment['writer'],
                    'negative_point' => $comment['negative_point']
                ]);
                if (!$isSaved) {
                    Log::error('Error saving comment: ' . $comment);
                }
            }
            
            return response()->json(['message' => 'Comments saved successfully']);
        }catch(\Exception $e){
            return response()->json(['message' => 'Error saving comment', 'error' => $e->getMessage()]);
        }
    }
}
