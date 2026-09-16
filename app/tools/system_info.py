import platform
import psutil
from pydantic import BaseModel
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel

class EmptyArgs(BaseModel):
    pass

class GetSystemInfoTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_system_info"
        
    @property
    def description(self) -> str:
        return "Gets safe, read-only system information like OS, CPU, and RAM usage."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.SAFE
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return EmptyArgs

    def _execute(self) -> ToolResult:
        try:
            # Gather safe system info
            os_name = f"{platform.system()} {platform.release()}"
            cpu_info = platform.processor()
            cpu_usage = psutil.cpu_percent(interval=0.1)
            
            ram = psutil.virtual_memory()
            ram_total_gb = round(ram.total / (1024**3), 2)
            ram_used_gb = round(ram.used / (1024**3), 2)
            ram_percent = ram.percent
            
            disk = psutil.disk_usage('/')
            disk_total_gb = round(disk.total / (1024**3), 2)
            disk_used_gb = round(disk.used / (1024**3), 2)
            disk_percent = disk.percent
            
            info_str = (
                f"Operating System: {os_name}\n"
                f"CPU: {cpu_info} (Usage: {cpu_usage}%)\n"
                f"RAM: {ram_used_gb} GB used out of {ram_total_gb} GB ({ram_percent}%)\n"
                f"Main Disk: {disk_used_gb} GB used out of {disk_total_gb} GB ({disk_percent}%)"
            )
            
            battery = psutil.sensors_battery()
            if battery:
                plugged = "Plugged in" if battery.power_plugged else "On battery"
                info_str += f"\nBattery: {battery.percent}% ({plugged})"
                
            return ToolResult(
                success=True, 
                message=f"System information retrieved successfully:\n{info_str}",
                data={
                    "os": os_name,
                    "cpu_usage": cpu_usage,
                    "ram_percent": ram_percent,
                    "disk_percent": disk_percent
                }
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to retrieve system info: {e}")
