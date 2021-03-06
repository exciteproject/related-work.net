package net.relatedwork.server.guice;

import com.gwtplatform.dispatch.server.guice.HandlerModule;

import net.relatedwork.server.action.*;
import net.relatedwork.shared.dto.*;
import net.relatedwork.server.action.NewUserActionActionHandler;
import net.relatedwork.shared.dto.DisplayPaper;
import net.relatedwork.server.action.DisplayPaperActionHandler;
import net.relatedwork.server.action.RequestGlobalSearchSuggestionActionHandler;
import net.relatedwork.server.action.RequestLocalSearchSuggestionActionHandler;
import net.relatedwork.server.action.UserVerifyActionActionHandler;
import net.relatedwork.shared.dto.SetAuthorMetaDataActionHandler;
import net.relatedwork.server.action.SetAuthorMetaDataActionHandlerActionHandler;

public class ServerModule extends HandlerModule {

	@Override
	protected void configureHandlers() {

		bindHandler(RequestGlobalSearchSuggestion.class,
				RequestGlobalSearchSuggestionActionHandler.class);

		bindHandler(DisplayAuthor.class, DisplayAuthorActionHandler.class);

		bindHandler(GlobalSearch.class, GlobalSearchActionHandler.class);

		bindHandler(LoginAction.class, LoginActionActionHandler.class);

		bindHandler(RequestLocalSearchSuggestion.class,
				RequestLocalSearchSuggestionActionHandler.class);
		


		bindHandler(NewUserAction.class, NewUserActionActionHandler.class);

		bindHandler(DisplayPaper.class, DisplayPaperActionHandler.class);

		bindHandler(UserVerifyAction.class, UserVerifyActionActionHandler.class);

		bindHandler(SetAuthorMetaDataActionHandler.class,
				SetAuthorMetaDataActionHandlerActionHandler.class);

		bindHandler(NewCommentAction.class, NewCommentActionHandler.class);

        bindHandler(CommentVoteAction.class, CommentVoteActionHandler.class);
	}
}
