package net.relatedwork.client.tools.events;

import net.relatedwork.shared.dto.AuthorSidebar;

import com.google.gwt.event.shared.GwtEvent;
import com.google.gwt.event.shared.EventHandler;
import com.google.gwt.event.shared.HasHandlers;

public class SidebarReloadedEvent extends
		GwtEvent<SidebarReloadedEvent.SidebarReloadedHandler> {

	public static Type<SidebarReloadedHandler> TYPE = new Type<SidebarReloadedHandler>();

	public interface SidebarReloadedHandler extends EventHandler {
		void onSidebarReloaded(SidebarReloadedEvent event);
	}

	private AuthorSidebar authorSidebar;


	
	public SidebarReloadedEvent() {
	}

	
	public SidebarReloadedEvent(AuthorSidebar asb) {
		this.authorSidebar = asb;
	}

	public AuthorSidebar getAuthorSidebar() {
		return authorSidebar;
	}


	public void setAuthorSidebar(AuthorSidebar authorSidebar) {
		this.authorSidebar = authorSidebar;
	}


	@Override
	protected void dispatch(SidebarReloadedHandler handler) {
		handler.onSidebarReloaded(this);
	}

	@Override
	public Type<SidebarReloadedHandler> getAssociatedType() {
		return TYPE;
	}

	public static Type<SidebarReloadedHandler> getType() {
		return TYPE;
	}

	public static void fire(HasHandlers source) {
		source.fireEvent(new SidebarReloadedEvent());
	}
}
