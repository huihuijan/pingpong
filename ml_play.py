"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        #else:
        #    return "MOVE_LEFT"

        ball = scene_info['ball']
        ballSpeed = scene_info['ball_speed']
        platform_1P = (scene_info['platform_1P'][0]+20, scene_info['platform_1P'][1])
        platform_2P = (scene_info['platform_2P'][0]+20, scene_info['platform_2P'][1]+30)

        self.pred = 100 # center
        if self.side == '1P':
            if(ballSpeed[1] > 0):  # ball move toward 1P platform
                self.pred = ball[0] + ((420 - ball[1]) // ballSpeed[1] ) * ballSpeed[0]

                if self.pred > 400:
                    self.pred = self.pred - 400
                elif self.pred < 400 and self.pred >200 :
                    self.pred = 200 - (self.pred -200 )
                elif self.pred < -200:
                    self.pred = 200 - (abs(self.pred) - 200)
                elif self.pred > -200 and self.pred < 0 :
                    self.pred = abs(self.pred)

                if self.pred > platform_1P[0]+5:
                    return "MOVE_RIGHT"
                elif self.pred < platform_1P[0]-5:
                    return "MOVE_LEFT"
                else:
                    return "NONE"
        else: #2P
            if(ballSpeed[1] < 0):  # ball move toward 2P platform
                self.pred = ball[0] + ((ball[1]-80) // abs(ballSpeed[1]) ) * ballSpeed[0]

                if self.pred > 400:
                    self.pred = self.pred - 400
                elif self.pred < 400 and self.pred >200 :
                    self.pred = 200 - (self.pred -200 )
                elif self.pred < -200:
                    self.pred = 200 - (abs(self.pred) - 200)
                elif self.pred > -200 and self.pred < 0 :
                    self.pred = abs(self.pred)

                if self.pred > platform_2P[0]+5:
                    return "MOVE_RIGHT"
                elif self.pred < platform_2P[0]-5:
                    return "MOVE_LEFT"
                else:
                    return "NONE"

        

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
