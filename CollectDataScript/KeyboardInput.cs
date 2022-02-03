using UnityEngine;

namespace KartGame.KartSystems {

    public class KeyboardInput : BaseInput
    {
        public string Horizontal = "Horizontal";
        public string Vertical = "Vertical";

        public override Vector2 GenerateInput() {
            
            var x_from_api = ColectData.GetX();
            var y_from_api = ColectData.GetY();
            return new Vector2 {
                //x = Input.GetAxis(Horizontal),
                x = x_from_api,
                //y = Input.GetAxis(Vertical)
                y = y_from_api
            };
        }
    }
}
