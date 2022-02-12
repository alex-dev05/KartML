#define ML
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
#if (ML)
                x = x_from_api,
                y = y_from_api
#else
                x = Input.GetAxis(Horizontal),
                y = Input.GetAxis(Vertical)
#endif


            };
        }
    }
}
