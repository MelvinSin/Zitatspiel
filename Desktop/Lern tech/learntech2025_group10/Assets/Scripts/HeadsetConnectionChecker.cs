using UnityEngine;

public class HeadsetConnectionChecker : MonoBehaviour
{
    private bool connected = false;
    void Start()
    {
        connected = UnityEngine.XR.InputDevices.GetDeviceAtXRNode(UnityEngine.XR.XRNode.Head).isValid;
        Debug.Log("Headset connected? " + connected);
    }
}
