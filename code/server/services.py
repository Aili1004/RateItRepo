import endpoints

import protocol

application = endpoints.api_server([protocol.RateItRestApi])
